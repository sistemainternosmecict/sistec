import hashlib
from datetime import datetime
from models.solicitantes import Solicitante_model

class Mensageiro:
    def __init__(self) -> None:
        self.__remetente:str = None
        self.__destinatario:str = None
        self.__assunto:str = None
        self.__mensagem:str = None

    def setar_dados_da_mensagem(self, dados:dict) -> None:
        if 'remetente' in dados:
            self.__remetente = dados['remetente']
        if 'destinatario' in dados:
            self.__destinatario = dados['destinatario']
        if 'assunto' in dados:
            self.__assunto = dados['assunto']
        if 'mensagem' in dados:
            self.__mensagem = dados['mensagem']

    def enviar_mensagem(self) -> bool:
        if self.__mensagem != None:
            return True
        return False

class Ferramentas:
    def __init__(self) -> None:
        self.__data_hora = datetime.now()

    def gerar_protocolo(self) -> int:
        agora_ano = str(self.__data_hora.year)
        agora_mes = f'{self.__data_hora.month:02}'
        agora_dia = f'{self.__data_hora.day:02}'
        agora_hora = f'{self.__data_hora.hour:02}'
        agora_minuto = f'{self.__data_hora.minute:02}'
        agora_segundo = f'{self.__data_hora.second:02}'
        self.__data_hora_formatada = agora_ano + agora_mes + agora_dia + agora_hora + agora_minuto + agora_segundo
        return int(self.__data_hora_formatada)

    def encriptar_senha(self, senha:str) -> str:
        sha512_hash = hashlib.sha3_512(senha.encode()).hexdigest()
        return sha512_hash[:100]
    
    def obter_data_hoje(self) -> dict:
        return {"data_hora":self.__data_hora}
    
    def criar_mensageiro(self) -> Mensageiro:
        self.__mensageiro = Mensageiro()
        return self.__mensageiro
    
    def enviar_mensagem(self, dados:dict) -> dict:
        self.__mensageiro.setar_dados_da_mensagem(dados)
        resultado = self.__mensageiro.enviar_mensagem()
        return {'email_enviado':resultado}
    
    def para_dict(self, obj:object, excluir_campos:list=None) -> dict:
        if excluir_campos is None:
            excluir_campos = []
        if hasattr(obj, '__table__'):
            return {column.name: getattr(obj, column.name) for column in obj.__table__.columns if column.name not in excluir_campos}
        else:
            return obj.__dict__
        
    def prepara_demanda_para_insercao_planilha( self, protocolo, dados ) -> list:
        retorno = [
            protocolo,
            "0",
            self.__data_hora.strftime("%d/%m/%Y"),
            "-",
            self.obter_solicitante_por_id(dados['solicitante']),
            dados['tipo'],
            dados['direcionamento'],
            dados['local'],
            dados['sala'],
            dados['descricao'],
            "Nova demanda"
        ]

        return retorno
    
    def prepara_demanda_para_atualizacao_planilha( self, dados ) -> list:
        retorno = [
            dados['protocolo'],
            dados['nvl_prioridade'],
            dados['dt_entrada'],
            "-",
            self.obter_solicitante_por_id(dados['solicitante']),
            dados['tipo'],
            dados['direcionamento'],
            dados['local'],
            dados['sala'],
            dados['descricao'],
            dados['status']
        ]

        return retorno
    
    def acertar_tipo_demanda(self, tipo_int:int) -> str:
        match tipo_int:
            case 0:
                return "Interna"
            case 1:
                return "Externa"
            
    def acertar_status_demanda(self, status_int:int) -> str:
        match status_int:
            case 1:
                return "Nova demanda"
            case 2:
                return "andamento"
            case 3:
                return "aguardando"
            case 4:
                return "encaminhada"
            case 5:
                return "finalizada"
            case 6:
                return "encerrada"
            
    def obter_solicitante_por_id( self, id_solicitante:int) -> str:
        solic_model = Solicitante_model()
        solic_model.solic_id = id_solicitante
        solic = solic_model.ler()
        return solic.solic_nome