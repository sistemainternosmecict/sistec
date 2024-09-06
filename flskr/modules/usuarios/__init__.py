from flask import Blueprint, jsonify, request
from ....modules.usuarios import Gerenciador_usuarios, Colaborador, Solicitante, Autenticador
from ....models.colaboradores import Colaborador_model

bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')

bp_colabs = Blueprint('colaboradores', __name__, url_prefix='/colaboradores')
bp_solic = Blueprint('solicitantes', __name__, url_prefix='/solicitantes')

bp_usuarios.register_blueprint(bp_colabs)
bp_usuarios.register_blueprint(bp_solic)

@bp_colabs.route("/listar")
def obter_colaboradores():
    GU = Gerenciador_usuarios()
    colab = GU.obter_todos_os_colaboradores()
    return jsonify({'colab':colab})

@bp_colabs.route("/buscar/<int:colab_id>")
def buscar_colab(colab_id):
    GU = Gerenciador_usuarios()
    resultado = GU.carregar_colaborador_via_id(colab_id)
    return jsonify({'colab':resultado})

@bp_colabs.route("/atualizar", methods=["POST"])
def atualizar_colaborador():
    dados = request.json
    GD = Gerenciador_usuarios()
    colab = GD.carregar_colaborador_via_id(dados['colab_id'])
    colab['usuario_nome'] = colab.pop('colab_nome')
    colab['usuario_sala'] = colab.pop('colab_sala')
    colab['usuario_email'] = colab.pop('colab_email')
    colab['usuario_telefone'] = colab.pop('colab_telefone')
    colab_obj = Colaborador(colab)
    dados.pop("colab_id")
    resultado = colab_obj.atualizar_colaborador(dados)
    print(colab_obj)
    return jsonify(resultado)

@bp_colabs.route("/registrar", methods=["POST"])
def registrar_colaborador():
    dados = request.json
    GD = Gerenciador_usuarios()
    resultado = GD.registrar_colaborador(dados)
    return jsonify(resultado)