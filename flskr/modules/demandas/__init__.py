from flask import Blueprint, jsonify, request
from ....modules.demandas import Gerenciador_demandas, Demanda

bp_demandas = Blueprint('demandas', __name__, url_prefix='/demandas')

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
    return jsonify(resultado)

@bp_demandas.route("/registrar", methods=["POST"])
def registrar_demanda():
    dados = request.json
    GD = Gerenciador_demandas()
    resultado = GD.criar_nova_demanda(dados)
    return jsonify(resultado)