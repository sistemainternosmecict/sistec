from flask import Blueprint, jsonify, request, session
from modules.usuarios import Gerenciador_usuarios, Autenticador, Usuario, GerenciadorNiveisAcesso, GerenciadorPermissoes, Gerenciador_rap
from modules.utilidades.lista_rh import Lista_rh

bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')
bp_auth = Blueprint('auth', __name__, url_prefix='/auth')
bp_niveis_acesso = Blueprint('niveis_acesso', __name__, url_prefix='/niveis_acesso')
bp_permissoes = Blueprint('permissoes', __name__, url_prefix='/permissoes')
bp_rap = Blueprint('rap', __name__, url_prefix='/rap')
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
    GU = Gerenciador_usuarios()
    dados = request.json
    matricula_temp = dados['usuario_matricula'].split('-')[0]
    # matricula_temp_sem_ultimo = matricula_temp[:-1]
    LRH = Lista_rh()
    resultado = LRH.buscar_por_matricula(dados['usuario_matricula'])
    print("2 -->", resultado)
    if resultado:
        todos_usuarios = GU.obter_todos_os_usuarios()
        if len(todos_usuarios['usuarios']) > 0:
            for usuario in todos_usuarios['usuarios']:
                if usuario['usuario_matricula'] == matricula_temp:
                    return jsonify({"msg":"Matricula já cadastrada!"})
        return jsonify(resultado)
    return jsonify({'msg':'A matrícula inserida não foi encontrada em nosso banco de dados! Dirija-se ao CPD da Secretaria de Educação (sala24) para realizar o seu cadastro.'})

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

########################################################################################################################
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

#####################################################################################################################
@bp_niveis_acesso.route('/listar', methods=['GET'])
def obter_niveis_acesso():
    GNA = GerenciadorNiveisAcesso()
    lista = GNA.listar_niveis_acessos()
    return jsonify(lista)

@bp_niveis_acesso.route('/buscar/<int:nivel_acesso_id>', methods=['GET'])
def buscar_nivel_acesso(nivel_acesso_id):
    GNA = GerenciadorNiveisAcesso()
    nivel_acesso = GNA.buscar_nivel(nivel_acesso_id)
    dados = nivel_acesso.obter_dados()
    return jsonify(dados)

@bp_niveis_acesso.route('/atualizar', methods=['POST'])
def atualizar_nivel_acesso():
    dados = request.json
    GNA = GerenciadorNiveisAcesso()
    nivel_acesso = GNA.buscar_nivel(dados['nva_id'])
    if nivel_acesso:
        resultado = nivel_acesso.atualizar(dados)
        return jsonify(resultado)
    return jsonify({'msg':'Nivel de acesso não encontrado!'})

@bp_niveis_acesso.route('/remover', methods=['POST'])
def remover_nivel_acesso():
    dados = request.json
    GNA = GerenciadorNiveisAcesso()
    resultado = GNA.remover_nivel(dados["nva_id"])
    return jsonify(resultado)

#################################################################################################################

@bp_permissoes.route('/registrar', methods=['POST'])
def registrar_permissao():
    dados = request.json
    GP = GerenciadorPermissoes()
    resultado = GP.registrar_permissao(dados)
    return jsonify(resultado)

@bp_permissoes.route("/listar", methods=['GET'])
def listar_permissoes():
    GP = GerenciadorPermissoes()
    lista = GP.obter_permissoes()
    return jsonify(lista)

@bp_permissoes.route("/buscar/<int:permissao_id>", methods=['GET'])
def buscar_permissao(permissao_id):
    GP = GerenciadorPermissoes()
    permissao = GP.buscar_permissao(permissao_id)
    dados = permissao.obter_dados()
    return jsonify(dados)

@bp_permissoes.route("/atualizar", methods=['POST'])
def atualizar_permissao():
    dados = request.json
    GP = GerenciadorPermissoes()
    permissao = GP.buscar_permissao(dados['perm_id'])
    if permissao:
        resultado = permissao.atualizar(dados)
        return jsonify(resultado)
    return jsonify({'msg':'Permissão não encontrada!'})

########################################################################################################

@bp_rap.route('/listar')
def listar_rap():
    GR = Gerenciador_rap()
    lista = GR.listar_relacoes_acesso_perm()
    return jsonify({'resultados':lista})

@bp_rap.route('/registrar', methods=["POST"])
def registrar_rap():
    dados = request.json
    GR = Gerenciador_rap()
    
    # Se o campo 'ativo' não for passado, vamos adicionar o valor padrão True
    if 'ativo' not in dados:
        dados['ativo'] = False
    
    resultado = GR.registrar_relacao_acesso_perm(dados)
    return jsonify(resultado)


@bp_rap.route('/atualizar', methods=["POST"])
def atualizar_rap():
    dados = request.json
    rap_id = dados.get('rap_id')
    novos_dados = {key: value for key, value in dados.items() if key != 'rap_id'}

    if not rap_id:
        return jsonify({'atualizado': False, 'msg': 'ID do relacionamento (rap_id) não fornecido.'}), 400

    if not novos_dados:
        return jsonify({'atualizado': False, 'msg': 'Nenhum dado para atualizar fornecido.'}), 400
    
    GR = Gerenciador_rap()
    resultado = GR.atualizar_relacao_acesso_perm(rap_id, novos_dados)
    return jsonify(resultado)


@bp_rap.route('/remover', methods=["POST"])
def remover_rap():
    dados = request.json
    GR = Gerenciador_rap()
    resultado = GR.remover_relacao_acesso_perm(dados['rap_id'])
    return jsonify(resultado)