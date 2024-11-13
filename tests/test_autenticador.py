from modules.usuarios import Autenticador

def mock() -> dict:
    mock_dict = {}
    mock_dict["usuario_matricula"] = 1234
    mock_dict["usuario_senha"] = "root"
    
    return mock_dict

def test_instanciando():
        instancia = Autenticador()
        assert isinstance(instancia, Autenticador)

def test_login():
        instancia = Autenticador()
        resposta = instancia.login(mock())
        assert resposta['auth'] == True
