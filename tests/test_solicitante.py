from modules.usuarios import Solicitante

def mock(com_id:bool=False) -> dict:
    mock_dict = {}
    
    mock_dict["usuario_cpf"] = 12345678910
    mock_dict["usuario_nome"] = "Usuario de teste com nome completo escrito por extenso"
    mock_dict["usuario_matricula"] = 123456
    mock_dict["usuario_setor"] = "TI"
    mock_dict["usuario_sala"] = "24"
    mock_dict["usuario_cargo"] = 1
    mock_dict["usuario_email"] = "mail_teste@mail.com"
    mock_dict["usuario_telefone"] = 22900000000
    mock_dict["usuario_senha"] = "root"
    mock_dict["usuario_tipo"] = 1
    mock_dict["usuario_ativo"] = True

    if com_id:
        mock_dict["usuario_id"] = 1
    
    return mock_dict

def test_instanciando():
    instancia = Solicitante(mock())
    assert isinstance(instancia, Solicitante)

def test_registro_comum():
    instancia = Solicitante()
    resultado = instancia.registrar_solicitante(mock())
    assert resultado['registro'] == True

def test_atualizar_cpf():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_cpf':33355544478})
    assert resultado['atualizado'] == True

def test_atualizar_nome():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_nome':'test'})
    assert resultado['atualizado'] == True

def test_atualizar_matricula():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_matricula':11122})
    assert resultado['atualizado'] == True

def test_atualizar_setor():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_setor':'ADM'})
    assert resultado['atualizado'] == True

def test_atualizar_sala():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_sala':'10'})
    assert resultado['atualizado'] == True

def test_atualizar_cargo():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_cargo':2})
    assert resultado['atualizado'] == True

def test_atualizar_email():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_email':'mail_novo@mail.com'})
    assert resultado['atualizado'] == True

def test_atualizar_telefone():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_telefone':123})
    assert resultado['atualizado'] == True

def test_atualizar_senha():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_senha':'senha_nova'})
    assert resultado['atualizado'] == True

def test_atualizar_tipo():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_tipo':2})
    assert resultado['atualizado'] == True 

def test_atualizar_ativo():
    instancia = Solicitante(mock(True))
    resultado = instancia.atualizar_solicitante({'usuario_ativo':False})
    assert resultado['atualizado'] == True 

# #somente para testes
def test_remover_solicitante():
    instancia = Solicitante(mock(True))
    resultado = instancia.remover_solicitante()
    assert resultado['removido'] == True