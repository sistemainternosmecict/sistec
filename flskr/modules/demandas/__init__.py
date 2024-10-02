from flask import Blueprint, jsonify, request
from modules.demandas import Gerenciador_demandas
from modules.demandas.autenticadorGDrive import Autenticador
from modules.demandas.gsheet import GSheetManager
from modules.utilidades.ferramentas import Ferramentas
import threading

bp_demandas = Blueprint('demandas', __name__, url_prefix='/demandas')

def executar_insercao_demanda( resultado_insercao:dict, dados:dict):
    FERRAMENTAS = Ferramentas()
    AUTH = Autenticador()
    GSHEET = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
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
        
    if linha_n != None:
        if dados['dem_status'] > 1 and dados['dem_status'] < 5:
            GSHEET.transferir_dados_entre_abas(linha_n, "demandas")
        elif dados['dem_status'] >= 5:
            GSHEET.transferir_dados_entre_abas(linha_n, "os_finalizadas")


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