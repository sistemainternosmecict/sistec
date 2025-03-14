from models.demandas import Demanda_model
from datetime import datetime
from modules.utilidades.ferramentas import Ferramentas

class Demanda:
    def __init__(self, dados: dict):
        self.nvl_prioridade = dados.get('nvl_prioridade') or 0
        self.link_oficio = dados.get('link_oficio') or None
        self.solicitante = dados.get('solicitante')
        self.tipo = dados.get('tipo')
        self.direcionamento = dados.get('direcionamento')
        self.descricao = dados.get('descricao')


        if not 'dt_entrada' in dados:
            data_atual = datetime.now()
            self.dt_entrada = data_atual.strftime("%d/%m/%Y|%H:%M")
        else:
            self.dt_entrada = dados.get("dt_entrada")
        if 'dt_atendimento' in dados:
            self.dt_atendimento = dados['dt_atendimento']
        if 'local' in dados:
            self.local = dados['local']
        if 'sala' in dados:
            self.sala = dados['sala']
        if 'protocolo' in dados:
            self.protocolo = dados['protocolo']
        if 'dt_final' in dados:
            self.dt_final = dados['dt_final']
        if 'tempo_finalizacao' in dados:
            self.tempo_finalizacao = dados['tempo_finalizacao']
        if 'atendido_por' in dados:
            self.atendido_por = dados['atendido_por']
        if 'observacoes' in dados:
            self.observacoes = dados['observacoes']
        if 'status' in dados:
            self.status = dados['status']

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
            'dt_atendimento': self.dt_atendimento,
            'solicitante': self.solicitante,
            'tipo': self.tipo,
            'direcionamento': self.direcionamento,
            'local': self.local,
            'sala': self.sala,
            'descricao': self.descricao,
            'status': self.status,
            'dt_final': self.dt_final,
            'atendido_por': self.atendido_por,
            'tempo_finalizacao': self.tempo_finalizacao,
            'observacoes': self.observacoes,
            'link_oficio': self.link_oficio
        }
        
        return dados

    def registrar_nova_demanda(self):
        ferramentas = Ferramentas()
        modelo = Demanda_model()
        modelo.dem_protocolo=ferramentas.gerar_protocolo()
        modelo.dem_solicitante_id=self.solicitante
        modelo.dem_direcionamento_id=self.direcionamento
        modelo.dem_dt_entrada=self.dt_entrada
        modelo.dem_dt_atendimento=None
        modelo.dem_tipo_demanda=self.tipo
        modelo.dem_local=self.local
        modelo.dem_sala=self.sala
        modelo.dem_descricao=self.descricao
        modelo.dem_status=self.status
        modelo.dem_prioridade=self.nvl_prioridade
        modelo.dem_dt_final=None
        modelo.dem_atendido_por_id=None
        modelo.dem_tempo_finalizacao=None
        modelo.dem_observacoes=None
        modelo.dem_link_oficio=self.link_oficio
        return modelo.inserir()

    def atualizar_demanda(self, dados: dict):
        modelo = Demanda_model()
        if 'protocolo' in dados:
            return modelo.atualizar(**dados)

    def finalizar_demanda(self, dados: dict):
        self.definir_status(dados['dem_status'])
        return self.atualizar_demanda(dados)

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
                dem_temp = Demanda(demanda)
                return dem_temp.obter_dados()
        return None
    
    def obter_obj_demanda_via_protocolo(self, protocolo: int) -> Demanda:
        for demanda in self.__demandas_lista:
            if demanda['protocolo'] == protocolo:
                dem_temp = Demanda(demanda)
                return dem_temp
        return None

    # def notificar_colab(self, msg: str) -> bool:
    #     ferramenta = Ferramentas()
    #     return ferramenta.enviar_mensagem(self.__colaborador, msg)

    def carregar_todas_as_demandas(self):
        modelo = Demanda_model()
        demandas_db = modelo.ler_todos()
        for dados in demandas_db:
            nova_demanda = Demanda({
                'protocolo': dados.dem_protocolo,
                'nvl_prioridade': dados.dem_prioridade,
                'dt_entrada': dados.dem_dt_entrada,
                'dt_atendimento': dados.dem_dt_atendimento,
                'solicitante': dados.dem_solicitante_id,
                'tipo': dados.dem_tipo_demanda,
                'local': dados.dem_local,
                'sala': dados.dem_sala,
                'direcionamento': dados.dem_direcionamento_id,
                'descricao': dados.dem_descricao,
                'status': dados.dem_status,
                'dt_final': dados.dem_dt_final,
                'atendido_por': dados.dem_atendido_por_id,
                'tempo_finalizacao': dados.dem_tempo_finalizacao,
                'observacoes': dados.dem_observacoes
            })
            self.agregar_demanda(nova_demanda.obter_dados())

    def obter_demandas_via_status(self, status: str) -> list:
        return [demanda for demanda in self.__demandas_lista if demanda.status == status]
