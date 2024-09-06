from flask import Blueprint, jsonify, request
from ....modules.demandas import Gerenciador_demandas, Demanda

bp_demandas = Blueprint('demandas', __name__, url_prefix='/demandas')

bp_interna = Blueprint('interna', __name__, url_prefix='/interna')
bp_externa = Blueprint('externa', __name__, url_prefix='/externa')

bp_demandas.register_blueprint(bp_interna)
bp_demandas.register_blueprint(bp_externa)

@bp_interna.route("/listar")
def obter_demandas():
    GD = Gerenciador_demandas()
    demandas = GD.obter_demandas()
    return jsonify({'demandas':demandas})

@bp_interna.route("/buscar/<int:protocolo>")
def obter_demanda(protocolo):
    GD = Gerenciador_demandas()
    demanda = GD.obter_demanda_via_protocolo(protocolo)
    return jsonify({'demandas':demanda})

@bp_interna.route("/atualizar", methods=["POST"])
def atualizar_demanda():
    dados = request.json
    GD = Gerenciador_demandas()
    demanda = GD.obter_demanda_via_protocolo(dados['protocolo'])
    resultado = demanda.atualizar_demanda(dados)
    return jsonify(resultado)

@bp_interna.route("/registrar", methods=["POST"])
def registrar_demanda():
    dados = request.json
    GD = Gerenciador_demandas()
    resultado = GD.criar_nova_demanda(dados)
    return jsonify(resultado)