from models.usuarios import Usuario_model
from modules.utilidades.ferramentas import Ferramentas

class Usuario:
    def __init__(self, dados : dict=None) -> None:
        if dados:
            if 'usuario_id' in dados:
                self.usuario_id = dados['usuario_id']

    def obter_dados(self):
        atributos = vars(self)
        return atributos
            
    def registrar_usuario(self, dados:dict)-> dict:
        model = Usuario_model(dados)
        return model.registrar_novo_usuario()

    def atualizar_usuario(self, dados:dict) -> dict:
        model = Usuario_model()
        resposta = model.atualizar_usuario(**dados)
        return resposta

    def remover_usuario(self) -> bool:
        model = Usuario_model()
        model.usuario_id = self.usuario_id
        resultado = model.remover_usuario()
        return resultado

    def usuario_existe(self, nome : str, sala : str) -> bool:
        solic_model = Usuario_model()
        resultado = solic_model.verificar(nome, sala)
        return {'usuario_existe':resultado}
    
    def obter_id(self) -> int:
        if hasattr(self, '_Usuario__id'):
            return self.__id
        return 0
    
    def obter_usuario(self):
        return {chave: valor for chave, valor in self.__dict__.items()}

class Autenticador:
    def login(self, credenciais:list):
        ferramentas = Ferramentas()
        self.usuario_matricula, self.usuario_senha = credenciais
        auth = self.autenticar()

        if auth['auth'] and auth['usuario']:
            dados_em_dict = ferramentas.para_dict(auth, ['usuario_senha'])
            return {'auth':True, 'usuario':dados_em_dict, 'msg':auth['msg']}
        return auth
          
    def autenticar(self):
        model = Usuario_model()
        auth = {'msg':'Este usuário não existe em nosso banco de dados!', 'auth':False}

        if (self.usuario_matricula == "") and (self.usuario_senha == ""):
            return {'msg':'Não é possível enviar campos vazios!', 'auth':False}
        
        resultado = model.verificar_credenciais(self.usuario_matricula, self.usuario_senha)
        auth = {'auth':resultado['verificado'], 'usuario':resultado['usuario'] if 'usuario' in resultado else None, 'msg':resultado['msg']}

        return auth

    def modelo_para_dict(self, obj:object, excluir_campos:list=None) -> dict:
        if excluir_campos is None:
            excluir_campos = []
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns if column.name not in excluir_campos}

    def logout(self):
        return {'logout':True}

class Gerenciador_usuarios:
    _listaRh = "./listaRh.xlsx"
    def verificar_campos(self, dados : dict) -> list:
        lista_campos = []
        campos_obrigatorios = ['usuario_cpf', 'usuario_nome', 'usuario_matricula', 'usuario_setor', 'usuario_sala', 'usuario_email', 'usuario_telefone']
        
        for campo in campos_obrigatorios:
            if not campo in dados:
                lista_campos.append(campo)
        return lista_campos
    
    def registrar_usuario(self, dados : dict) -> dict:
        usuario = Usuario()
        resultado = usuario.registrar_usuario(dados)
        return resultado
    
    def carregar_usuario_via_id(self, solic_id : int) -> dict:
        ferramentas = Ferramentas()
        model = Usuario_model()
        usuario = model.ler_pelo_id(solic_id)
        resultado = ferramentas.para_dict(usuario, ['usuario_senha'])
        return resultado
    
    def remover_usuario_via_id(self, usuario_id:int) -> dict:
        dados = {'usuario_id':usuario_id}
        model = Usuario_model(dados)
        resultado = model.remover_usuario(usuario_id)
        return resultado
    
    def obter_todos_os_usuarios(self):
        usuarios_temp = []
        model = Usuario_model()
        usuarios = model.ler_todos_os_registros()
        for usuario in usuarios['todos_usuarios']:
            usuario_dict = {
                "usuario_id":usuario.usuario_id,
                "usuario_cpf":usuario.usuario_cpf,
                "usuario_nome":usuario.usuario_nome,
                "usuario_matricula":usuario.usuario_matricula,
                "usuario_setor":usuario.usuario_setor,
                "usuario_sala":usuario.usuario_sala,
                "usuario_cargo":usuario.usuario_cargo,
                "usuario_funcao":usuario.usuario_funcao,
                "usuario_telefone":usuario.usuario_telefone,
                "usuario_email":usuario.usuario_email,
                "usuario_tipo":usuario.usuario_tipo,
                "usuario_ativo":usuario.usuario_ativo
            }
            usuarios_temp.append(usuario_dict)
        return {"usuarios":usuarios_temp}