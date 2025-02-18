
from dotenv import load_dotenv
from models.unidades import Unidade_model 

load_dotenv()

class Unidade:
    def __init__(self, dados: dict = None):
        self.dados = dados
        if self.dados:
            for chave, valor in self.dados.items():
                setattr(self, chave, valor)
        self.model = Unidade_model()

    def criar_unidade(self):
        self.model.uni_registro = self.uni_registro
        self.model.uni_cod_ue = self.uni_cod_ue
        self.model.uni_designador_categoria = self.uni_designador_categoria
        self.model.uni_nome = self.uni_nome
        self.model.uni_cep = self.uni_cep
        nova_unidade = self.model.criar_unidade()
        return nova_unidade
    
    def ler_unidade_por_id(self, uni_id:int) -> dict:
        unidade_encontrada = self.model.buscar_por_id(uni_id)
        return {column: getattr(unidade_encontrada['unidade'], column) for column in unidade_encontrada['unidade'].__table__.columns.keys()}
    
    def ler_unidade_por_cod_ue(self, uni_cod_ue:int) -> dict:
        unidade_encontrada = self.model.buscar_por_cod_ue(uni_cod_ue)
        return {column: getattr(unidade_encontrada['unidade'], column) for column in unidade_encontrada['unidade'].__table__.columns.keys()}
    
    def ler_unidade_por_designador_categoria(self, uni_designador_categoria:str) -> list:
        unidade_encontrada = self.model.buscar_por_categoria(uni_designador_categoria)
        lista_retorno = []
        for unidade in unidade_encontrada['unidades']:
            lista_retorno.append({column: getattr(unidade, column) for column in unidade.__table__.columns.keys()})
        return lista_retorno
    
    def atualizar_unidade(self, novos_dados:dict):
        return self.model.atualizar_unidade(novos_dados)
    
    def remover_unidade(self, uni_id:int):
        unidade = self.model.buscar_por_id(uni_id)
        resultado = self.model.remover_unidade(unidade['unidade'])
        return resultado
    
    def ativar_unidade(self, uni_id:int):
        return self.model.ativar_unidade(uni_id)

    def desativar_unidade(self, uni_id:int):
        return self.model.desativar_unidade(uni_id)
    
    def ler_todos(self, ordem:str=None):
        resultado = self.model.ler_todos(ordem)
        lista_retorno = []
        for unidade in resultado:
            lista_retorno.append({column: getattr(unidade, column) for column in unidade.__table__.columns.keys()})
        return lista_retorno