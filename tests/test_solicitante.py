from modules.usuarios import Solicitante

def test_solicitante_instanciando():
    mock_dados_sem_id = {
        "usuario_nome":"test user",
        "usuario_sala":"0001",
        "usuario_email":"testmail1@mail.com",
        "usuario_telefone":"0"
    }
    instancia_solicitante = Solicitante(mock_dados_sem_id)
    assert isinstance(instancia_solicitante, Solicitante)

def test_solicitante_obter_dados_retorna_dados_em_dict():
    mock_dados_sem_id = {
        "usuario_nome":"test user",
        "usuario_sala":"0001",
        "usuario_email":"testmail1@mail.com",
        "usuario_telefone":"0"
    }
    instancia_solicitante = Solicitante(mock_dados_sem_id)
    resultado = instancia_solicitante.obter_dados()
    assert type(resultado) == dict

# Teste de registro e de remoção

def test_solicitante_registrar_solicitante_1_funciona():
    mock_dados_sem_id = {
        "usuario_nome":"test user",
        "usuario_sala":"0001",
        "usuario_email":"testmail1@mail.com",
        "usuario_telefone":"0"
    }
    instancia_solicitante = Solicitante(mock_dados_sem_id)
    resultado = instancia_solicitante.registrar_solicitante("root", "test")
    assert resultado['id'] == 1
    assert resultado['registro'] == True

def test_solicitante_instanciar_com_id_retorna_id():
    mock_dados_com_id = {
        "usuario_nome":"test user",
        "usuario_sala":"1000",
        "usuario_email":"testmail1@mail.com",
        "usuario_telefone":"0",
        "solic_id":1
    }
    instancia_solicitante = Solicitante(mock_dados_com_id)
    resultado = instancia_solicitante.obter_id()
    assert resultado > 0

def test_solicitante_atualizar_com_dados_corretos():
    mock_dados_com_id = {
        "usuario_nome":"test user",
        "usuario_sala":"1000",
        "usuario_email":"testmail1@mail.com",
        "usuario_telefone":"0",
        "solic_id":1
    }
    mock_dados_atualizados = {
        "solic_nome":"admin",
        "solic_sala":"24",
        "solic_senha":"senha_trocada"
    }
    instancia_solicitante = Solicitante(mock_dados_com_id)
    resultado = instancia_solicitante.atualizar_solicitante(mock_dados_atualizados)
    assert resultado['atualizado'] == True

def test_solicitante_registrar_solicitante_2_funciona():
    mock_dados_sem_id = {
        "usuario_nome":"test user2",
        "usuario_sala":"200",
        "usuario_email":"testmail2@mail.com",
        "usuario_telefone":"999"
    }
    instancia_solicitante2 = Solicitante(mock_dados_sem_id)
    resultado = instancia_solicitante2.registrar_solicitante("user2","senhateste")
    assert resultado['id'] == 2
    assert resultado['registro'] == True

def test_solicitante_remover_solicitante_1_do_banco():
    mock_dados_com_id = {
        "usuario_nome":"test user",
        "usuario_sala":"1000",
        "usuario_email":"testmail1@mail.com",
        "usuario_telefone":"0",
        "solic_id":1
    }
    instancia_solicitante1 = Solicitante(mock_dados_com_id)
    resultado1 = instancia_solicitante1.remover_solicitante()
    assert resultado1['removido'] == True

def test_solicitante_registrar_solicitante_email_cadastrado():
    mock_dados_sem_id = {
        "usuario_nome":"test user2",
        "usuario_sala":"200",
        "usuario_email":"testmail2@mail.com",
        "usuario_telefone":"999"
    }
    instancia_solicitante2 = Solicitante(mock_dados_sem_id)
    resultado = instancia_solicitante2.registrar_solicitante("user2","senhateste")
    assert "O email" in resultado['msg']
    assert "já está cadastrado" in resultado['msg']

def test_solicitante_registrar_solicitante_retorno_de_erro():
    dados = {
        "usuario_nome":"testando_um_nome_muito_longo_para_dar_erro",
        "usuario_sala":10029129,
        "usuario_email":None,
        "usuario_telefone":999329873298732
    }
    instancia_solicitante = Solicitante(dados)
    resultado = instancia_solicitante.registrar_solicitante("test","test")
    assert "Não foi possível" in resultado['msg']

def test_solicitante_existe_retorna_verdadeiro_quando_usuario_existe():
    mock_dados_com_id = {
        "usuario_nome":"test user2",
        "usuario_sala":"200",
        "usuario_email":"testmail2@mail.com",
        "usuario_telefone":"999",
        "solic_id":1
    }
    instancia_solicitante = Solicitante(mock_dados_com_id)
    resultado = instancia_solicitante.usuario_existe(mock_dados_com_id['usuario_nome'], mock_dados_com_id['usuario_sala'])
    assert resultado['usuario_existe'] == True

def test_solicitante_existe_retorna_falso_quando_usuario_nao_existe():
    mock_dados_com_id = {
        "usuario_nome":"test user2",
        "usuario_sala":"200",
        "usuario_email":"testmail2@mail.com",
        "usuario_telefone":"999",
        "solic_id":1
    }
    instancia_solicitante = Solicitante(mock_dados_com_id)
    resultado = instancia_solicitante.usuario_existe('usuario_inexistente', 'sala_inexistente')
    assert resultado['usuario_existe'] == False

def test_solicitante_retorna_true_quando_remover_usuario_2():
    mock_dados_com_id = {
        "usuario_nome":"test user2",
        "usuario_sala":"200",
        "usuario_email":"testmail2@mail.com",
        "usuario_telefone":"999",
        "solic_id":2
    }
    instancia_solicitante1 = Solicitante(mock_dados_com_id)
    resultado1 = instancia_solicitante1.remover_solicitante()
    assert resultado1['removido'] == True
