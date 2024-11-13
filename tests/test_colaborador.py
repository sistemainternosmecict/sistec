from ..modules.usuarios import Colaborador

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
    instancia = Colaborador(mock())
    assert isinstance(instancia, Colaborador)

def test_registro_comum():
    instancia = Colaborador()
    resultado = instancia.registrar_colaborador(mock())
    assert resultado['registro'] == True

def test_nao_registra_nome_usuario_igual():
    instancia = Colaborador()
    resultado = instancia.registrar_colaborador(mock())
    assert resultado['registro'] == False

def test_atualizar_cpf():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_cpf':33355544478})
    assert resultado['atualizado'] == True

def test_atualizar_nome():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_nome':'test'})
    assert resultado['atualizado'] == True

def test_atualizar_matricula():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_matricula':11122})
    assert resultado['atualizado'] == True

def test_atualizar_setor():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_setor':'ADM'})
    assert resultado['atualizado'] == True

def test_atualizar_sala():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_sala':'10'})
    assert resultado['atualizado'] == True

def test_atualizar_cargo():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_cargo':2})
    assert resultado['atualizado'] == True

def test_atualizar_email():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_email':'mail_novo@mail.com'})
    assert resultado['atualizado'] == True

def test_atualizar_telefone():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_telefone':123})
    assert resultado['atualizado'] == True

def test_atualizar_senha():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_senha':'senha_nova'})
    assert resultado['atualizado'] == True

def test_atualizar_tipo():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_tipo':2})
    assert resultado['atualizado'] == True 

def test_atualizar_ativo():
    instancia = Colaborador(mock(True))
    resultado = instancia.atualizar_colaborador({'usuario_ativo':False})
    assert resultado['atualizado'] == True 

# #somente para testes
def test_remover_colaborador():
    instancia = Colaborador(mock(True))
    resultado = instancia.remover_colaborador()
    assert resultado['removido'] == True