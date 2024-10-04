from models.solicitantes import Solicitante_model

def construct_model(model:object, type:int) -> object:
    if type == 1:
        model.solic_id = 1
        model.solic_nome = "test user"
        model.solic_sala = "0001"
        model.solic_email = "testmail@mail.com"
        model.solic_telefone = "0"
        model.solic_nome_usuario = "root"
        model.solic_senha = "senha_teste"
        model.solic_ativo = False
    return model

def test_colaboradores_retorna():
    instancia = Solicitante_model()
    assert instancia

def test_model_solicitante_printa_repr():
    instancia_solicitante = Solicitante_model()
    instancia = construct_model(instancia_solicitante, 1)
    assert repr(instancia) == "<Solicitante(solic_id=1, solic_nome=test user, solic_sala=0001, solic_email=testmail@mail.com, solic_telefone=0, solic_nome_usuario=root, solic_ativo=False)>"

def test_solicitante_insere_normalmente():
    instancia_solicitante = Solicitante_model()
    instancia = construct_model(instancia_solicitante, 1)
    resultado = instancia.criar()
    assert resultado['registro'] == True

def test_modificar_solic_ativo_funciona():
    instancia_solicitante = Solicitante_model()
    instancia = construct_model(instancia_solicitante, 1)
    instancia.solic_id = 1
    resultado = instancia.atualizar(solic_ativo=True)
    assert resultado == True

def test_modificar_solic_senha_funciona():
    instancia_solicitante = Solicitante_model()
    instancia = construct_model(instancia_solicitante, 1)
    instancia.solic_id = 1
    resultado = instancia.atualizar(solic_senha="test")
    assert resultado == True

def test_ler_retorna_dados_corretamente():
    instancia_solicitante = Solicitante_model()
    instancia_solicitante.solic_id = 1
    instancia = instancia_solicitante.ler()
    ativo = instancia.solic_ativo
    assert ativo == True