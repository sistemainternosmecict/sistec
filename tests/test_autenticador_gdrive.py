from modules.demandas.autenticadorGDrive import Autenticador, gspread

def test_intanciando_normalmente():
    AUTH = Autenticador()
    assert isinstance(AUTH, Autenticador)

def test_lendo_credencial_json():
    AUTH = Autenticador()
    AUTH._ler()
    assert type(AUTH.obter_credenciais()) == dict

def test_conexao_de_cliente_funciona():
    AUTH = Autenticador()
    AUTH.conectar()
    cliente = AUTH.obter_cliente()
    assert type(cliente) == gspread.client.Client