import hashlib
from datetime import datetime

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

    def gerar_protocolo(self, demanda_id) -> int:
        self.__data_hora_formatada = self.__data_hora.strftime("%Y%m%d")
        return int(f"{self.__data_hora_formatada}{demanda_id}")

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
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns if column.name not in excluir_campos}