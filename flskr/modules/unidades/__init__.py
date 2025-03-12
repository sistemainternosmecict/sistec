from flask import Blueprint, jsonify, request
from modules.unidades import Unidade, Sala, Sala_model

bp_unidades = Blueprint('unidades', __name__, url_prefix='/unidades')
bp_salas = Blueprint('salas', __name__, url_prefix='/salas')

@bp_unidades.route("/listar", methods=["GET"])
def listar_unidades():
    model = Unidade()
    resultado = model.ler_todos()
    return jsonify({"unidades":resultado})

@bp_unidades.route("/registrar", methods=["POST"])
def criar_unidade():
    dados = request.json
    model = Unidade(dados)
    resultado = model.criar_unidade()
    return jsonify(resultado)

@bp_unidades.route("/buscar/cod_ue/<uni_cod_ue>", methods=["GET"])
def buscar_por_cod_ue(uni_cod_ue):
    model = Unidade()
    resultado = model.ler_unidade_por_cod_ue(uni_cod_ue)
    return jsonify(resultado)

@bp_unidades.route("/buscar/id/<uni_id>", methods=["GET"])
def buscar_por_id(uni_id):
    model = Unidade()
    resultado = model.ler_unidade_por_id(uni_id)
    return jsonify(resultado)

@bp_unidades.route("/buscar/categorias/<uni_designador_categoria>", methods=["GET"])
def buscar_por_categoria(uni_designador_categoria):
    model = Unidade()
    resultado = model.ler_unidade_por_designador_categoria(uni_designador_categoria)
    return jsonify(resultado)

@bp_unidades.route("/atualizar", methods=["POST"])
def atualizar_unidade():
    dados = request.json
    model = Unidade()
    resultado = model.atualizar_unidade(dados)
    return jsonify(resultado)

@bp_unidades.route("/remover", methods=["POST"])
def remover_unidade():
    dados = request.json
    model = Unidade()
    id = dados['uni_id']
    resultado = model.remover_unidade(id)
    return jsonify(resultado)

# ROTAS para as salas das unidades

@bp_salas.route('/registrar', methods=['POST'])
def criar_sala():
    dados = request.get_json()
    sala = Sala(dados)
    result = sala.criar()
    return jsonify(result), 201 if result['registro'] else 400

@bp_salas.route('/buscar/<int:id>', methods=['GET'])
def buscar_sala(id):
    sala = Sala_model()
    result = sala.buscar_por_id(id)
    return jsonify(result), 200 if result['encontrado'] else 404

@bp_salas.route('/buscar/unidade/<int:uni_id>', methods=['GET'])
def buscar_salas_por_uni(uni_id):
    sala = Sala_model()
    result = sala.buscar_por_uni_id(uni_id)
    return jsonify(result), 200 if result['encontrado'] else 404

@bp_salas.route('/listar', methods=['GET'])
def ler_salas():
    ordem = request.args.get('ordem', 'id_unico_sala')
    sala = Sala({})
    salas = sala.ler_todas(ordem)
    return jsonify(salas)

@bp_salas.route('/atualizar/<int:id>', methods=['PUT'])
def atualizar_sala(id):
    dados = request.get_json()
    updates = {'id_unico_sala': id, **dados}
    sala = Sala_model()
    result = sala.atualizar_sala(updates)
    return jsonify(result), 200 if result['atualizado'] else 400

@bp_salas.route('/remover/<int:id>', methods=['DELETE'])
def remover_sala(id):
    sala = Sala()
    result = sala.remover(id)
    return jsonify(result), 200 if result['removido'] else 404
