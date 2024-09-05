from modules.usuarios import Usuario

mock_dados = {
        "usuario_nome":"test user",
        "usuario_sala":"1000",
        "usuario_email":"testmail@mail.com",
        "usuario_telefone":"0"
    }

# testar se está instanciando com dados basico

def test_usuario_instanciando():
    instancia_usuario = Usuario(mock_dados)
    assert isinstance(instancia_usuario, Usuario)

# testar se os dados correspondem ao inserido

def test_usuario_obter_dados_retorna_dados_em_dict():
    instancia_usuario = Usuario(mock_dados)
    resultado = instancia_usuario.obter_dados()
    assert type(resultado) == dict