from ...models.demandas import Demanda_model
# from models.demandas import Demanda_model #somente nos testes
from datetime import datetime
from ...modules.utilidades.ferramentas import Ferramentas
# from modules.utilidades.ferramentas import Ferramentas #somente nos testes

class Demanda:
    def __init__(self, dados: dict):
        data_atual = datetime.now()
        self.nvl_prioridade = dados.get('nvl_prioridade')
        self.dt_entrada = data_atual.strftime("%d/%m/%Y")
        self.solicitante = dados.get('solicitante')
        self.tipo = dados.get('tipo')
        self.direcionamento = dados.get('direcionamento')
        self.local = dados.get('local')
        self.descricao = dados.get('descricao')
        self.status = dados.get('status')
        self.dt_final = None
        self.atendido_por = None
        self.tempo_finalizacao = None
        if 'protocolo' in dados:
            self.protocolo = dados['protocolo']

    def definir_np(self, np: int):
        self.nvl_prioridade = int(np)

    def definir_direcionamento(self, direc: str):
        self.direcionamento = direc

    def definir_status(self, status: str):
        self.status = status

    def obter_dados(self) -> dict:
        dados = {
            'protocolo': self.protocolo,
            'nvl_prioridade': self.nvl_prioridade,
            'dt_entrada': self.dt_entrada,
            'solicitante': self.solicitante,
            'tipo': self.tipo,
            'direcionamento': self.direcionamento,
            'local': self.local,
            'descricao': self.descricao,
            'status': self.status,
            'dt_final': self.dt_final,
            'atendido_por': self.atendido_por,
            'tempo_finalizacao': self.tempo_finalizacao
        }
        
        return dados

    def registrar_nova_demanda(self):
        ferramentas = Ferramentas()
        modelo = Demanda_model()
        modelo.dem_protocolo=ferramentas.gerar_protocolo()
        modelo.tb_solicitantes_id=self.solicitante
        modelo.tb_colaboradores_id=self.direcionamento
        modelo.dem_dt_entrada=self.dt_entrada
        modelo.dem_tipo_demanda=self.tipo
        modelo.dem_local=self.local
        modelo.dem_descricao=self.descricao
        modelo.dem_status=1
        modelo.dem_prioridade=self.nvl_prioridade
        modelo.dem_dt_final=None
        modelo.dem_atendido_por=None
        modelo.dem_tempo_finalizacao=None
        modelo.dem_observacoes=None
        modelo.dem_link_oficio=None
        return modelo.inserir()

    def atualizar_demanda(self, dados: dict):
        modelo = Demanda_model()
        if 'protocolo' in dados:
            return modelo.atualizar(**dados)

    def finalizar_demanda(self, dados: dict):
        self.definir_status(dados['status'])
        return self.atualizar_demanda({'dem_status': dados['status'], 'protocolo':dados['protocolo']})

class Gerenciador_demandas:
    def __init__(self):
        self.__demandas_lista = []
        self.carregar_todas_as_demandas()

    def criar_nova_demanda(self, dados:dict):
        demanda = Demanda(dados)
        resultado = demanda.registrar_nova_demanda()
        if resultado['inserido'] == True:
            self.__demandas_lista.append(demanda)
        return resultado

    def agregar_demanda(self, demanda: Demanda) -> dict:
        self.__demandas_lista.append(demanda)
        return {'agregada': True}

    def obter_demandas(self) -> list:
        return self.__demandas_lista

    def obter_demanda_via_protocolo(self, protocolo: int) -> Demanda:
        for demanda in self.__demandas_lista:
            if demanda['protocolo'] == protocolo:
                return Demanda(demanda)
        return None

    def notificar_colab(self, msg: str) -> bool:
        ferramenta = Ferramentas()
        return ferramenta.enviar_mensagem(self.__colaborador, msg)

    def carregar_todas_as_demandas(self):
        modelo = Demanda_model()
        demandas_db = modelo.ler_todos()
        for dados in demandas_db:
            nova_demanda = Demanda({
                'protocolo': dados.dem_protocolo,
                'nvl_prioridade': dados.dem_prioridade,
                'dt_entrada': dados.dem_dt_entrada,
                'solicitante': dados.tb_solicitantes_id,
                'tipo': dados.dem_tipo_demanda,
                'direcionamento': dados.dem_local,
                'descricao': dados.dem_descricao,
                'status': dados.dem_status,
                'dt_final': dados.dem_dt_final,
                'atendido_por': dados.dem_atendido_por,
                'tempo_finalizacao': dados.dem_tempo_finalizacao
            })
            self.agregar_demanda(nova_demanda.obter_dados())

    def obter_demandas_via_status(self, status: str) -> list:
        return [demanda for demanda in self.__demandas_lista if demanda.status == status]
