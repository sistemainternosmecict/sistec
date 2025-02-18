from modules.unidades import Unidade

mock = {
    "uni_registro":"18/02/2025",
    "uni_cod_ue":10,
    "uni_designador_categoria":"C.M.E.",
    "uni_nome":"Padre Manuel",
    "uni_cep":28990000
}

def test_instanciacao():
    instancia = Unidade(mock)
    assert type(instancia) == Unidade

def test_insercao_normal():
    esperado = {"msg":"Registro realizado!", "registro":True, "id_registrado":27}
    instancia = Unidade(mock)
    resultado = instancia.criar_unidade()
    assert resultado == esperado

def test_leitura_por_id():
    instancia = Unidade()
    resultado = instancia.ler_unidade_por_id(11)
    assert type(resultado) == dict

def test_leitura_por_cod_ue():
    instancia = Unidade()
    resultado = instancia.ler_unidade_por_cod_ue(10)
    assert type(resultado) == dict

def test_leitura_por_designador_categoria():
    instancia = Unidade()
    resultado = instancia.ler_unidade_por_designador_categoria("C.M.E.")
    assert type(resultado) == list

def test_atualizar_unidade():
    esperado = {'atualizado':True}
    instancia = Unidade()
    resultado = instancia.atualizar_unidade({"uni_id":20, "uni_designador_categoria":"E.Municipalizada"})
    assert resultado == esperado

def test_ativar_unidade():
    esperado = {"ativada":True, "msg":"Unidade ativada com sucesso!"}
    instancia = Unidade()
    resultado = instancia.ativar_unidade(20)
    assert resultado == esperado

def test_desativar_unidade():
    esperado = {"ativada":False, "msg":"Unidade desativada com sucesso!"}
    instancia = Unidade()
    instancia.ativar_unidade(22)
    resultado = instancia.desativar_unidade(22)
    assert resultado == esperado

def test_remocao_normal():
    esperado = { "msg":"Registro removido!", "removido":True }
    instancia = Unidade()
    resultado = instancia.remover_unidade(22)
    assert resultado == esperado