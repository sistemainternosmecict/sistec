from ...models.solicitantes import Solicitante_model
from ...models.colaboradores import Colaborador_model
from ...modules.utilidades.ferramentas import Ferramentas

class Usuario:
    def __init__(self, dados : dict) -> None:
        self.__nome = dados['usuario_nome']
        self.__sala = dados['usuario_sala']
        self.__email = dados['usuario_email']
        self.__telefone = dados['usuario_telefone']

    def obter_dados(self):
        atributos = vars(self)
        return atributos

class Solicitante(Usuario):
    __solicitacoes_realizadas: int

    def __init__(self, dados : dict) -> None:
        super().__init__(dados)
        if 'solic_id' in dados:
            self.__id:int = dados['solic_id']

    def registrar_solicitante(self):
        solic_model = Solicitante_model()
        solic_model.solic_nome = self._Usuario__nome
        solic_model.solic_sala = self._Usuario__sala
        solic_model.solic_email = self._Usuario__email
        solic_model.solic_telefone = self._Usuario__telefone
        return solic_model.criar()

    def atualizar_solicitante(self, dados : dict) -> dict:
        solic_model = Solicitante_model()
        solic_model.solic_id = self._Solicitante__id
        solicitante_atualizado = solic_model.atualizar(**dados)
        return {'atualizado':solicitante_atualizado}

    def remover_solicitante(self) -> bool:
        solic_model = Solicitante_model()
        solic_model.solic_id = self._Solicitante__id
        solicitante_deletado = solic_model.deletar()
        return {'removido':solicitante_deletado}

    def usuario_existe(self, nome : str, sala : str) -> bool:
        solic_model = Solicitante_model()
        resultado = solic_model.verificar(nome, sala)
        return {'usuario_existe':resultado}
    
    def obter_id(self) -> int:
        if hasattr(self, '_Solicitante__id'):
            return self.__id
        return 0

class Colaborador(Usuario):
    def __init__(self, dados: dict) -> None:
        super().__init__(dados)
        if 'colab_id' in dados:
            self.id:int = dados['colab_id']
    
    def registrar_colaborador(self, colab_nome_usuario:str, colab_senha:str):
        colab_model = Colaborador_model()
        ferramentas = Ferramentas()
        colab_model.colab_sala = self._Usuario__sala
        colab_model.colab_nome = self._Usuario__nome
        colab_model.colab_nome_usuario = colab_nome_usuario
        colab_model.colab_email = self._Usuario__email
        colab_model.colab_telefone = self._Usuario__telefone
        colab_model.colab_senha = ferramentas.encriptar_senha(colab_senha)
        colab_model.colab_ativo = False
        return colab_model.criar()

    def atualizar_colaborador(self, dados:dict) -> dict:
        colab_model = Colaborador_model()
        colab_model.colab_id = self.id
        colaborador_atualizado = colab_model.atualizar(**dados)
        return {'atualizado':colaborador_atualizado}

    def remover_colaborador(self) -> bool:
        colab_model = Colaborador_model()
        colab_model.colab_id = self.id
        colaborador_removido = colab_model.deletar()
        return {'removido':colaborador_removido}
    
    def obter_colab(self):
        return {chave: valor for chave, valor in self.__dict__.items()}

class Autenticador:
    def login(self, credenciais:list):
        self.nome_usuario, self.senha = credenciais
        auth = self.autenticar()
        if auth['auth']:
            if auth['colab'] != None:
                dados_em_dict = self.modelo_para_dict(auth['colab'])
                return {'login':True, 'colab':auth['colab'], 'usuario_dict':dados_em_dict}
        return auth
          
    def autenticar(self):
        ferramentas = Ferramentas()
        senha_hash = ferramentas.encriptar_senha(self.senha)
        colab_model = Colaborador_model()
        if (self.nome_usuario == "") and (self.senha == ""):
            return {'msg':'Não é possível enviar campos vazios!', 'auth':False}
        if colab_model.colab_existe(self.nome_usuario) == None:
            return {'msg':'Este usuário não existe em nosso banco de dados!', 'auth':False}
        colab = colab_model.login(self.nome_usuario, senha_hash)
        if colab != None:
            return {'auth':True, 'colab':colab}
        return {'msg':'Senha incorreta','auth':False}

    def modelo_para_dict(self, obj:object, excluir_campos:list=None) -> dict:
        if excluir_campos is None:
            excluir_campos = []
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns if column.name not in excluir_campos}

    def logout(self):
        return {'logout':True}

class Gerenciador_usuarios:
    def verificar_campos(self, dados : dict) -> list:
        lista_campos = []
        campos_obrigatorios = ['usuario_nome', 'usuario_sala', 'usuario_email', 'usuario_telefone']
        
        for campo in campos_obrigatorios:
            if not campo in dados:
                lista_campos.append(campo)
        return lista_campos
    
    def construir_solicitante(self, dados:dict) -> Solicitante:
        return Solicitante(dados)
    
    def construir_colaborador(self, dados:dict) -> Colaborador:
        return Colaborador(dados)
    
    def registrar_solicitante(self, dados : dict) -> dict:
        solic = self.construir_solicitante(dados)
        resultado = solic.registrar_solicitante()
        return {'res':resultado}
    
    def registrar_colaborador(self, dados:dict) -> dict:
        colab = self.construir_colaborador(dados)
        resultado = colab.registrar_colaborador(dados['colab_nome_usuario'], dados['colab_senha'])
        return {'res':resultado}
    
    def carregar_solicitante_via_id(self, solic_id : int) -> dict:
        ferramentas = Ferramentas()
        model = Solicitante_model()
        model.solic_id = solic_id
        resultado = model.ler()
        return {'dados':ferramentas.para_dict(resultado)}

    def carregar_colaborador_via_id(self, colab_id:int) -> object:
        ferramentas = Ferramentas()
        model = Colaborador_model()
        model.colab_id = colab_id
        resultado = model.ler()
        retorno = ferramentas.para_dict(resultado)
        retorno.pop("colab_senha", None)
        return retorno
    
    def remover_solicitante_via_id(self, solic_id:int) -> dict:
        model = Solicitante_model()
        model.solic_id = solic_id
        resultado = model.deletar()
        return {'removido':resultado}
    
    def obter_todos_os_colaboradores(self):
        usuarios = []
        model = Colaborador_model()
        colaboradores = model.let_tudo()
        for colab in colaboradores:
            colab_dict = {
                "colab_id":colab.colab_id,
                "colab_sala":colab.colab_sala,
                "colab_nome":colab.colab_sala,
                "colab_nome_usuario":colab.colab_nome_usuario,
                "colab_email":colab.colab_email,
                "colab_telefone":colab.colab_telefone,
                "colab_ativo":colab.colab_ativo
            }
            usuarios.append(colab_dict)
        return usuarios
    
    def obter_todos_os_solicitantes(self):
        usuarios = []
        model = Solicitante_model()
        solicitantes = model.ler_tudo()
        for solic in solicitantes:
            solic_dict = {
                "solic_id":solic.solic_id,
                "solic_nome":solic.solic_sala,
                "solic_sala":solic.solic_sala,
                "solic_email":solic.solic_email,
                "solic_telefone":solic.solic_telefone
            }
            usuarios.append(solic_dict)
        return usuarios