from flask import Blueprint, jsonify, request, session
from ....modules.usuarios import Gerenciador_usuarios, Colaborador, Solicitante, Autenticador
from ....models.colaboradores import Colaborador_model

bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')

bp_colabs = Blueprint('colaboradores', __name__, url_prefix='/colaboradores')
bp_solic = Blueprint('solicitantes', __name__, url_prefix='/solicitantes')
bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

bp_usuarios.register_blueprint(bp_colabs)
bp_usuarios.register_blueprint(bp_solic)
bp_usuarios.register_blueprint(bp_auth)

###################################
#
# ROTAS DE COLABORADORES
#
###################################

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
    if dados['colab_ativo'] == False:
        dados['colab_ativo']=0
    elif dados['colab_ativo'] == True:
        dados['colab_ativo']=1
    resultado = colab_obj.atualizar_colaborador(dados)
    return jsonify(resultado)

@bp_colabs.route("/registrar", methods=["POST"])
def registrar_colaborador():
    if request.is_json:
            dados = request.json
            GD = Gerenciador_usuarios()
            resultado = GD.registrar_colaborador(dados)
            return jsonify(resultado['res'])

###################################
#
# ROTAS DE SOLICITANTES
#
###################################

@bp_solic.route("/listar")
def obter_solicitantes():
    if 'usuario' in session:
        GU = Gerenciador_usuarios()
        colab = GU.obter_todos_os_solicitantes()
        return jsonify({'solics':colab})

@bp_solic.route("/buscar/<int:colab_id>")
def buscar_solicitante(colab_id):
    if 'usuario' in session:
        GU = Gerenciador_usuarios()
        resultado = GU.carregar_solicitante_via_id(colab_id)
        return jsonify({'colab':resultado})

@bp_solic.route("/atualizar", methods=["POST"])
def atualizar_solicitante():
    if 'usuario' in session:
        dados = request.json
        GD = Gerenciador_usuarios()
        solic_dados = GD.carregar_solicitante_via_id(dados['solic_id'])
        solic = solic_dados['dados']
        solic['usuario_nome'] = solic.pop('solic_nome')
        solic['usuario_sala'] = solic.pop('solic_sala')
        solic['usuario_email'] = solic.pop('solic_email')
        solic['usuario_telefone'] = solic.pop('solic_telefone')
        solic_obj = Solicitante(solic)
        dados.pop("solic_id")
        resultado = solic_obj.atualizar_solicitante(dados)
        return jsonify(resultado)

@bp_solic.route("/registrar", methods=["POST"])
def registrar_solicitante():
    if 'usuario' in session:
        dados = request.json
        GD = Gerenciador_usuarios()
        resultado = GD.registrar_solicitante(dados)
        return jsonify(resultado)

###################################
#
# ROTAS DE AUTENTICAÇÃO
#
###################################

@bp_auth.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.is_json:
        dados = request.json
        AUTH = Autenticador()
        resultado = AUTH.login([dados['colab_nome_usuario'], dados['colab_senha']])
        if resultado['auth'] == True:
            usuario = resultado['usuario_dict']
            session['usuario'] = usuario
        return jsonify(resultado)
    return "Tipo errado de payload"

@bp_auth.route('/logout', methods=['GET'])
def logout():
    session.pop('usuario', None)
    return jsonify({'msg':'Usuario deslogado!'})