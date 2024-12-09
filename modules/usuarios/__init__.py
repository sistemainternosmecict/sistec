from models.usuarios import Usuario_model
from modules.utilidades.ferramentas import Ferramentas
from models.niveis_acesso import NiveisAcesso_model
from models.permissoes import Permissao_model
from models.rel_acesso_perm import RelAcessoPermn_model

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
                "usuario_ativo":usuario.usuario_ativo,
                "usuario_vinculo":usuario.usuario_vinculo
            }
            usuarios_temp.append(usuario_dict)
        return {"usuarios":usuarios_temp}
    
class NivelDeAcesso:
    def __init__(self, dados: dict = None):
        if dados:
            for chave, valor in dados.items():
                setattr(self, chave, valor)

    def registrar(self):
        if(type(self.nva_nome) == str and type(self.nva_desc) == str):
            model = NiveisAcesso_model({"nva_nome":self.nva_nome, "nva_desc":self.nva_desc})
            return model.registrar_novo_nivel()
        return {'registro':False}

    def atualizar(self, dados:dict):
        model = NiveisAcesso_model()
        return model.atualizar_nivel(**dados)
    
    def remover(self):
        model = NiveisAcesso_model()
        return model.remover_nivel(self.nva_id)
    
    def obter_dados(self):
        return self.__dict__

class GerenciadorNiveisAcesso:
    def __init__(self):
        self.__niveis_acessos = []
        self.__carregar_dados()

    def __carregar_dados(self):
        model = NiveisAcesso_model()
        niveis = model.ler_todos_os_niveis()
        todos_niveis = niveis['todos_niveis']
        for model in todos_niveis:
            nivel = {
                "nva_id": model.nva_id,
                "nva_nome": model.nva_nome,
                "nva_desc": model.nva_desc
            }
            self.__niveis_acessos.append(nivel)

    def buscar_nivel(self, nva_id):
        for nivel in self.__niveis_acessos:
            if nivel["nva_id"] == nva_id:
                return NivelDeAcesso(nivel)
        return None

    def regitrar_novo_nivel(self, dados:dict=None):
        nivel_acesso = NivelDeAcesso(dados)
        resultado = nivel_acesso.registrar()
        self.__niveis_acessos.append({**nivel_acesso.obter_dados(), "nva_id":resultado['id']})
        return resultado
    
    def listar_niveis_acessos(self):
        return [nivel for nivel in self.__niveis_acessos]
    
    def atualizar_nivel(self, id:int, dados:dict):
        for nivel in self.__niveis_acessos:
            if nivel["nva_id"] == id:
                nivel["nva_nome"] = dados["nva_nome"]
                nivel["nva_desc"] = dados["nva_desc"]
                nivel_obj = NivelDeAcesso()
                return nivel_obj.atualizar(dados)
        return {'atualizado': False}
    
    def remover_nivel(self, id:int):
        for nivel in self.__niveis_acessos:
            if nivel["nva_id"] == id:
                self.__niveis_acessos.remove(nivel)
                nivel_obj = NivelDeAcesso({"nva_id": id})
                return nivel_obj.remover()
        return {'removido': False}
    
class Permissao:
    def __init__(self, dados: dict = None):
        if dados:
            for chave, valor in dados.items():
                setattr(self, chave, valor)

    def registrar(self):
        if(type(self.perm_nome) == str and type(self.perm_desc) == str):
            model = Permissao_model()
            return model.registrar({"perm_nome":self.perm_nome, "perm_desc":self.perm_desc})
        return {'registro':False}
    
    def atualizar(self, dados:dict):
        model = Permissao_model()
        return model.atualizar(**dados)
    
    def remover(self, perm_id:int):
        model = Permissao_model()
        return model.remover_permissao(perm_id)
    
    def ler_por_id(self, perm_id:int):
        model = Permissao_model()
        res = model.ler_por_id(perm_id)
        self.perm_id = res.perm_id
        self.perm_nome = res.perm_nome
        self.perm_desc = res.perm_desc
        return self
    
    def obter_dados(self):
        return self.__dict__
    
class GerenciadorPermissoes:
    def __init__(self):
        self.__permissoes = []
        self.__carregar_dados()

    def __carregar_dados(self):
        model = Permissao_model()
        permissoes = model.ler_todos()
        for perm in permissoes:
            temp = {"perm_id": perm.perm_id, "perm_nome": perm.perm_nome, "perm_desc":perm.perm_desc}
            self.__permissoes.append(Permissao(temp))

    def obter_permissoes(self):
        return [perm.obter_dados() for perm in self.__permissoes]
    
    def buscar_permissao(self, perm_id:int):
        for perm in self.__permissoes:
            if perm.perm_id == perm_id:
                return perm
        return None
    
    def registrar_permissao(self, dados: dict):
        perm = Permissao(dados)
        resultado = perm.registrar()
        self.__permissoes.append(perm)
        return resultado
    
    def atualizar_permissao(self, dados: dict):
        for perm in self.__permissoes:
            if perm.perm_id == dados['perm_id']:
                res = perm.atualizar(dados)
                if res['atualizado']:
                    if 'perm_nome' in dados:
                        perm.perm_nome = dados['perm_nome']
                    if 'perm_desc' in dados:
                        perm.perm_desc = dados['perm_desc']
                    return res
        return None
    
    def remover_permissao(self, perm_id: int):
        for idx, perm in enumerate(self.__permissoes):
            if perm.perm_id == perm_id:
                res = perm.remover(perm_id)
                if res['removido']:
                    self.__permissoes.pop(idx)
                    return res
        return None
    
class Rel_acesso_perm:
    def __init__(self, dados: dict = None):
        if dados:
            for chave, valor in dados.items():
                setattr(self, chave, valor)
    
    def registrar(self):
        if(type(self.rap_acesso_id) == int and type(self.rap_perm_id) == int):
            model = RelAcessoPermn_model({"rap_acesso_id":self.rap_acesso_id, "rap_perm_id":self.rap_perm_id})
            return model.registrar_novo_rel_acesso_perm()
        return {'registro':False}
    
    def remover(self):
        model = RelAcessoPermn_model()
        return model.remover_rel_acesso_perm(self.rap_id)
    
    def obter_dados(self):
        return self.__dict__
    
class Gerenciador_rap:
    def __init__(self):
        self.__relacoes_acesso_perm = []
        self.__carregar_dados()

    def __carregar_dados(self):
        model = RelAcessoPermn_model()
        relacoes = model.ler_todos()
        for relacao in relacoes:
            temp = {"rap_id": relacao.rap_id, "rap_acesso_id": relacao.rap_acesso_id, "rap_perm_id": relacao.rap_perm_id}
            self.__relacoes_acesso_perm.append(Rel_acesso_perm(temp))

    def listar_relacoes_acesso_perm(self):
        return [rel.obter_dados() for rel in self.__relacoes_acesso_perm]
    
    def obter_relacoes_acesso_perm(self):
        return [rel for rel in self.__relacoes_acesso_perm]
    
    def buscar_relacao_acesso_perm(self, rap_id:int):
        for rel in self.__relacoes_acesso_perm:
            if rel.rap_id == rap_id:
                return rel
        return None
    
    def registrar_relacao_acesso_perm(self, dados: dict):
        rel = Rel_acesso_perm(dados)
        resultado = rel.registrar()
        self.__relacoes_acesso_perm.append(rel)
        return resultado
    
    def remover_relacao_acesso_perm(self, rap_id: int):
        for idx, rel in enumerate(self.__relacoes_acesso_perm):
            if rel.rap_id == rap_id:
                res = rel.remover()
                if res['removido']:
                    self.__relacoes_acesso_perm.pop(idx)
                    return res
        return None