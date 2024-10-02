import json, os, gspread
from oauth2client.service_account import ServiceAccountCredentials

class Autenticador:
    _ESCOPOS = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
    _file_path = "./controledemandasti.json"

    def __init__(self) -> None:
        self._root_path = os.getcwd()
        self._ler()
        self.conectar()

    def _ler(self) -> dict:
        with open(self._file_path, 'r', encoding='utf-8') as arquivo:
            self._credenciais_dict = json.load(arquivo)

    def obter_credenciais(self) -> dict:
        return self._credenciais_dict
    
    def conectar(self):
        self._credenciais = ServiceAccountCredentials.from_json_keyfile_name(self._file_path, self._ESCOPOS)
        self._cliente = gspread.authorize(self._credenciais)
    
    def obter_cliente(self):
        return self._cliente