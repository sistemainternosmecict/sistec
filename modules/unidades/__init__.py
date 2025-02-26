
from dotenv import load_dotenv
from models.unidades import Unidade_model
from models.uni_salas import Sala_model

load_dotenv()

class Unidade:
    def __init__(self, dados: dict = None):
        self.dados = dados
        if self.dados:
            for chave, valor in self.dados.items():
                setattr(self, chave, valor)
        self.model = Unidade_model()

    def criar_unidade(self):
        if "uni_logradouro" in self.dados:
            self.model.uni_logradouro = self.uni_logradouro
        if "uni_bairro" in self.dados:
            self.model.uni_bairro = self.uni_bairro
        if "uni_numero_end" in self.dados:
            self.model.uni_numero_end = self.uni_numero_end
        
        self.model.uni_distrito = self.uni_distrito
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
    
class Sala:
    def __init__(self, dados):
        self.numero_sala = dados.get('numero_sala') if 'numero_sala' in dados else 0
        self.comprimento_sala = dados.get('comprimento_sala') if 'comprimento_sala' in dados else 0.0
        self.largura_sala = dados.get('largura_sala') if 'largura_sala' in dados else 0.0
        self.qnt_entradas = dados.get('qnt_entradas') if 'qnt_entradas' in dados else 0
        self.qnt_portas = dados.get('qnt_portas') if 'qnt_portas' in dados else 0
        self.qnt_janelas = dados.get('qnt_janelas') if 'qnt_janelas' in dados else 0
        self.qnt_tomadas = dados.get('qnt_tomadas') if 'qnt_tomadas' in dados else 0
        self.internet = dados.get('internet') if 'internet' in dados else 0
        self.tipo_sala = dados.get('tipo_sala') if 'tipo_sala' in dados else None
        self.sala_andar = dados.get('sala_andar') if 'sala_andar' in dados else 0
        self.uni_id = dados.get('uni_id') if 'uni_id' in dados else None

    def criar(self):
        sala_model = Sala_model()

        sala_model.comprimento_sala=self.comprimento_sala,
        sala_model.largura_sala=self.largura_sala,
        sala_model.tipo_sala=self.tipo_sala,
        sala_model.uni_id=self.uni_id
        # sala_model.numero_sala=self.numero_sala,
        # sala_model.qnt_entradas=self.qnt_entradas,
        # sala_model.qnt_portas=self.qnt_portas,
        # sala_model.qnt_janelas=self.qnt_janelas,
        # sala_model.qnt_tomadas=self.qnt_tomadas,
        # sala_model.internet=self.internet,
        # sala_model.sala_andar=self.sala_andar,

        return sala_model.criar_sala()

    def buscar_por_id(self, id):
        sala_model = Sala_model()
        return sala_model.buscar_por_id(id)

    def buscar_por_uni_id(self, uni_id):
        sala_model = Sala_model()
        return sala_model.buscar_por_uni_id(uni_id)

    def ler_todas(self, ordem='id_unico_sala'):
        sala_model = Sala_model()
        return sala_model.ler_todas(ordem)

    def atualizar(self, updates):
        sala_model = Sala_model()
        return sala_model.atualizar_sala(updates)

    def remover(self, id):
        sala_model = Sala_model()
        sala = sala_model.buscar_por_id(id)
        if sala['encontrado']:
            return sala_model.remover_sala(sala['sala'])
        return {"msg": "Sala não encontrada", "removido": False}