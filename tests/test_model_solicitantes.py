from models.solicitantes import Solicitante_model

def construct_model(model:object, type:int) -> object:
    if type == 1:
        model.solic_id = 1
        model.solic_nome = "test user"
        model.solic_sala = "1000"
        model.solic_email = "testmail@mail.com"
        model.solic_telefone = "0"
    return model

def test_colaboradores_retorna():
    instancia = Solicitante_model()
    assert instancia

def test_model_solicitante_printa_repr():
    instancia_solicitante = Solicitante_model()
    instancia = construct_model(instancia_solicitante, 1)
    assert repr(instancia) == "<Solicitante(solic_id=1, solic_nome=test user, solic_sala=1000, solic_email=testmail@mail.com, solic_telefone=0)>"