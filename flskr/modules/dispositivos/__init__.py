from flask import Blueprint, jsonify, request
from modules.dispositivos import GerenciadorDispositivos

bp_dispositivos = Blueprint('dispositivos', __name__, url_prefix='/dispositivos')

gerenciador = GerenciadorDispositivos()

@bp_dispositivos.route('/listar', methods=['GET'])
def listar_dispositivos():
    dispositivos = gerenciador.listar_dispositivos()
    return jsonify([{
        "disp_id": d.disp_id,
        "disp_serial": d.disp_serial,
        "disp_tipo": d.disp_tipo,
        "disp_desc": d.disp_desc
    } for d in dispositivos]), 200

@bp_dispositivos.route('/buscar/<disp_serial>', methods=['GET'])
def obter_dispositivo(disp_serial):
    dispositivo = gerenciador.buscar_dispositivo_por_serial(disp_serial)
    if not dispositivo:
        return jsonify({"erro": "Dispositivo não encontrado"}), 404
    return jsonify({
        "disp_id": dispositivo.disp_id,
        "disp_serial": dispositivo.disp_serial,
        "disp_tipo": dispositivo.disp_tipo,
        "disp_desc": dispositivo.disp_desc
    }), 200

@bp_dispositivos.route('/registrar', methods=['POST'])
def registrar_dispositivo():
    dados = request.json
    if not dados or not all(k in dados for k in ["disp_serial", "disp_tipo", "disp_desc"]):
        return jsonify({"erro": "Dados inválidos"}), 400

    novo_dispositivo = gerenciador.registrar_dispositivo(dados)

    return jsonify(novo_dispositivo)

@bp_dispositivos.route('/atualizar/<disp_serial>', methods=['PUT'])
def atualizar_dispositivo(disp_serial):
    novos_dados = request.json
    dispositivo_atualizado = gerenciador.atualizar_dispositivo(disp_serial, novos_dados)
    return jsonify(dispositivo_atualizado)

@bp_dispositivos.route('/remover/<int:disp_id>', methods=['DELETE'])
def remover_dispositivo(disp_id):
    if not gerenciador.remover_dispositivo(disp_id):
        return jsonify({"erro": "Dispositivo não encontrado"}), 404
    return jsonify({"mensagem": "Dispositivo removido com sucesso"}), 200
