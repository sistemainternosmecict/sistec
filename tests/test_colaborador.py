from modules.usuarios import Colaborador

mock_dados_colab = {
    "usuario_nome":"thyéz",
    "usuario_sala":"24",
    "usuario_email":"thyezolaiveira@gmail.com",
    "usuario_telefone":"22998548514",
    "colab_id":1
}

def test_colaborador_instanciando():
    instancia_colaborador = Colaborador(mock_dados_colab)
    assert isinstance(instancia_colaborador, Colaborador)

# Testar se o registro do colaborador esta registrando com os dados corretos

def test_colaborador_registrar_colaborador_funciona():
    instancia_colaborador = Colaborador(mock_dados_colab)
    resultado = instancia_colaborador.registrar_colaborador("thyez_s24", "senhateste")
    assert resultado['registro'] == True

# Testar se o registro do colaborador esta barrando o registro com nome de usuario repetido

def test_colaborador_registrar_colaborador_nao_registra_nome_usuario_igual():
    instancia_colaborador = Colaborador(mock_dados_colab)
    resultado = instancia_colaborador.registrar_colaborador("thyez_s24", "senhateste")
    assert resultado['registro'] == False

# Testar se a atualização do colaborador esta atualizando o nome, sala, email, telefone, ativo e senha

def test_colaborador_atualizar_nome():
    instancia_colaborador = Colaborador(mock_dados_colab)
    resultado = instancia_colaborador.atualizar_colaborador({'colab_nome':'test'})
    resultado = instancia_colaborador.atualizar_colaborador({'colab_nome':mock_dados_colab['usuario_nome']})
    assert resultado['atualizado'] == True


def test_colaborador_atualizar_sala():
    instancia_colaborador = Colaborador(mock_dados_colab)
    resultado = instancia_colaborador.atualizar_colaborador({'colab_sala':'test'})
    resultado = instancia_colaborador.atualizar_colaborador({'colab_sala':mock_dados_colab['usuario_sala']})
    assert resultado['atualizado'] == True

def test_colaborador_atualizar_email():
    instancia_colaborador = Colaborador(mock_dados_colab)
    resultado = instancia_colaborador.atualizar_colaborador({'colab_email':'test'})
    resultado = instancia_colaborador.atualizar_colaborador({'colab_email':mock_dados_colab['usuario_email']})
    assert resultado['atualizado'] == True

def test_colaborador_atualizar_telefone():
    instancia_colaborador = Colaborador(mock_dados_colab)
    resultado = instancia_colaborador.atualizar_colaborador({'colab_telefone':'test'})
    resultado = instancia_colaborador.atualizar_colaborador({'colab_telefone':mock_dados_colab['usuario_telefone']})
    assert resultado['atualizado'] == True

def test_colaborador_atualizar_ativo():
    instancia_colaborador = Colaborador(mock_dados_colab)
    resultado = instancia_colaborador.atualizar_colaborador({'colab_ativo':'test'})
    resultado = instancia_colaborador.atualizar_colaborador({'colab_ativo':False})
    assert resultado['atualizado'] == True 

def test_colaborador_atualizar_senha():
    instancia_colaborador = Colaborador(mock_dados_colab)
    resultado = instancia_colaborador.atualizar_colaborador({'colab_senha':'test'})
    resultado = instancia_colaborador.atualizar_colaborador({'colab_senha':"senhateste"})
    assert resultado['atualizado'] == True

#somente para testes
def test_solicitante_remover_colaborador_do_banco():
    instancia_colaborador = Colaborador(mock_dados_colab)
    resultado = instancia_colaborador.remover_colaborador()
    assert resultado['removido'] == True