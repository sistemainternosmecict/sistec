from models.uni_salas import Sala_model

def construct_model(com_id:bool=False) -> Sala_model:
    model = Sala_model()
    if com_id:
        model.id_unico_sala = 1
    model.numero_sala = 17
    model.comprimento_sala = 8.2
    model.largura_sala = 5.8
    model.uni_id = 5
    return model

def test_instanciacao_do_modelo():
    instancia = construct_model()
    assert type(instancia) == Sala_model

def test_insercao_normal():
    esperado = { "msg":"Registro realizado!", "registro":True, "id_registrado":4 }
    instancia = construct_model()
    resultado = instancia.criar_sala()
    assert resultado == esperado