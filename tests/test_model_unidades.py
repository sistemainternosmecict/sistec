from models.unidades import Unidade_model

def construct_model(com_id:bool=False) -> Unidade_model:
    model = Unidade_model()
    if com_id:
        model.uni_id = 1

    model.uni_cod_ue = 17
    model.uni_designador_categoria = "E.M."
    model.uni_nome = "Nome de teste"
    model.uni_cep = 28994744
    return model

def test_instanciacao_do_modelo():
    instancia = construct_model()
    assert type(instancia) == Unidade_model

# def test_insercao_normal():
#     esperado = { "msg":"Registro realizado!", "registro":True, "id_registrado":1 }
#     instancia = construct_model()
#     resultado = instancia.criar_unidade()
#     assert resultado == esperado

# def test_buscar_por_id():
#     instancia = construct_model(True)
#     resultado = instancia.buscar_por_id(instancia.uni_id)
#     assert type(resultado['unidade']) == Unidade_model
#     assert resultado['unidade'].uni_id == instancia.uni_id

def test_remocao_normal():
    esperado = { "msg":"Registro removido!", "removido":True }
    instancia = construct_model()
    instancia.uni_id = 2
    resultado = instancia.remover_unidade()
    assert resultado == esperado