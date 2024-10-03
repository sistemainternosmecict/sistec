from flask import Blueprint, jsonify, request
from modules.demandas import Gerenciador_demandas
from modules.demandas.autenticadorGDrive import Autenticador
from modules.demandas.gsheet import GSheetManager
from modules.utilidades.ferramentas import Ferramentas
from models.colaboradores import Colaborador_model
import threading

bp_demandas = Blueprint('demandas', __name__, url_prefix='/demandas')

def obter_colaborador_por_id( id_colaborador:int):
        colab_model = Colaborador_model()
        colab_model.colab_id = id_colaborador
        colab = colab_model.ler()
        if id_colaborador != 0:
            return colab.colab_nome
        return "N/D"

def executar_insercao_demanda( resultado_insercao:dict, dados:dict):
    FERRAMENTAS = Ferramentas()
    AUTH = Autenticador()
    GSHEET = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    dados['direcionamento'] = obter_colaborador_por_id(dados['direcionamento'])
    dados['tipo'] = FERRAMENTAS.acertar_tipo_demanda(dados['tipo'])
    dados_formatados = FERRAMENTAS.prepara_demanda_para_insercao_planilha(resultado_insercao['protocolo'], dados)
    GSHEET.inserir_dados(dados_formatados)

def executar_troca_status_demanda( demanda, dados ):
    FERRAMENTAS = Ferramentas()
    AUTH = Autenticador()
    demanda_temp = demanda.obter_dados()
    demanda_formatada = FERRAMENTAS.prepara_demanda_para_atualizacao_planilha(demanda_temp)
    status = FERRAMENTAS.acertar_status_demanda(dados['dem_status'])
    linha_n = None

    if demanda_formatada[-1] == 1:
        GSHEET = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
        linha_n = GSHEET.obter_linha_pelo_protocolo(demanda_formatada[0])
        GSHEET.atualizar_status(linha_n, status)
    
    if demanda_formatada[-1] > 1 and demanda_formatada[-1] < 5:
        GSHEET = GSheetManager("controle_demandas", "demandas", AUTH.obter_cliente())
        linha_n = GSHEET.obter_linha_pelo_protocolo(demanda_formatada[0])
        GSHEET.atualizar_status(linha_n, status)

@bp_demandas.route("/listar")
def obter_demandas():
    GD = Gerenciador_demandas()
    demandas = GD.obter_demandas()
    return jsonify({'demandas':demandas})

@bp_demandas.route("/buscar/<int:protocolo>")
def obter_demanda(protocolo):
    GD = Gerenciador_demandas()
    demanda = GD.obter_demanda_via_protocolo(protocolo)
    return jsonify({'demandas':demanda})

@bp_demandas.route("/atualizar", methods=["POST"])
def atualizar_demanda():
    dados = request.json
    GD = Gerenciador_demandas()
    demanda = GD.obter_demanda_via_protocolo(dados['protocolo'])
    resultado = demanda.atualizar_demanda(dados)

    if 'dem_status' in dados:
        thread_insercao_planilha = threading.Thread(target=executar_troca_status_demanda, args=(demanda, dados,))
        thread_insercao_planilha.start()
        
    return jsonify(resultado)

@bp_demandas.route("/registrar", methods=["POST"])
def registrar_demanda():
    dados = request.json
    GD = Gerenciador_demandas()
    resultado = GD.criar_nova_demanda(dados)

    thread_insercao_planilha = threading.Thread(target=executar_insercao_demanda, args=(resultado, dados,))
    thread_insercao_planilha.start()

    return jsonify(resultado)