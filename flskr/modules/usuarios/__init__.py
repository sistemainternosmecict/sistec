from flask import Blueprint, jsonify, request, session
from modules.usuarios import Gerenciador_usuarios, Autenticador, Usuario
from modules.utilidades.lista_rh import Lista_rh

bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')
bp_auth = Blueprint('auth', __name__, url_prefix='/auth')
bp_usuarios.register_blueprint(bp_auth)

@bp_usuarios.route("/listar")
def obter_usuarios():
    GU = Gerenciador_usuarios()
    resultado = GU.obter_todos_os_usuarios()
    return jsonify(resultado)

@bp_usuarios.route("/buscar/<int:usuario_id>")
def buscar_usuario(usuario_id):
    GU = Gerenciador_usuarios()
    resultado = GU.carregar_usuario_via_id(usuario_id)
    return jsonify(resultado)

@bp_usuarios.route("/atualizar", methods=["POST"])
def atualizar_usuarios():
    dados = request.json
    usuario = Usuario(dados)
    resultado = usuario.atualizar_usuario(dados)
    return jsonify(resultado)

@bp_usuarios.route("/validar/matricula", methods=["POST"])
def validar_matricula():
    dados = request.json
    LRH = Lista_rh()
    resultado = LRH.buscar_por_matricula(dados['usuario_matricula'])
    if resultado:
        return jsonify(resultado)
    return jsonify({'msg':'A matrícula iserida não foi encontrada em nosso banco de dados! Dirija-se ao CPD da Secretaria de Educação (sala24) para realizar o seu cadastro.'})

@bp_usuarios.route("/registrar", methods=["POST"])
def registrar_usuario():
    if request.is_json:
        dados = request.json
        GD = Gerenciador_usuarios()
        resultado = GD.registrar_usuario(dados)
        return jsonify(resultado)
    
@bp_usuarios.route("/remover", methods=["POST"])
def remover_usuario():
    dados = request.json
    GD = Gerenciador_usuarios()
    resultado = GD.remover_usuario_via_id(dados['usuario_id'])
    return jsonify(resultado)

@bp_auth.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.is_json:
        dados = request.json
        AUTH = Autenticador()
        resultado = AUTH.login([dados['usuario_matricula'], dados['usuario_senha']])
        if resultado['auth']:
            usuario = resultado['usuario']
            session['usuario'] = usuario
        return jsonify(resultado)
    return "Tipo errado de payload"

@bp_auth.route('/logout', methods=['GET'])
def logout():
    session.pop('usuario', None)
    return jsonify({'msg':'Usuario deslogado!'})