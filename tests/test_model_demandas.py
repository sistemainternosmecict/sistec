from models.demandas import Demanda_model

def construct_model(model:object, type:int) -> object:
    if type == 1:
        model.dem_protocolo = 1234567890
        model.tb_solicitantes_id = 1
        model.tb_colaboradores_id = 1
        model.dem_dt_entrada = "2024/09/18|12:00"
        model.dem_tipo_demanda = 1
        model.dem_local = "SMECICT"
        model.dem_sala = "24"
        model.dem_descricao = "Testando a descricao da demanda!"
        model.dem_status = 1
        model.dem_prioridade = 0
    return model

def test_instanciando():
    instancia = Demanda_model()
    assert instancia

def test_printa_repr():
    instancia_demanda_model = Demanda_model()
    instancia = construct_model(instancia_demanda_model, 1)
    assert "Demanda" in repr(instancia)

def test_registro_retorna_true_com_dados_corretos():
    instancia_demanda_model = Demanda_model()
    instancia = construct_model(instancia_demanda_model, 1)
    resposta = instancia.inserir()
    assert resposta['inserido'] == True

def test_registro_retorna_false_com_dados_incorretos():
    instancia_demanda_model = Demanda_model()
    instancia = construct_model(instancia_demanda_model, 1)
    instancia.dem_local = 2
    resposta = instancia.inserir()
    assert resposta['inserido'] == False

    instancia.dem_sala = 2
    resposta = instancia.inserir()
    assert resposta['inserido'] == False

def test_buscar_todos_os_registros_retorna_lista():
    instancia_demanda_model = Demanda_model()
    resposta = instancia_demanda_model.ler_todos()
    assert type(resposta) == list

def test_buscar_demandas_por_status_retorna_corretamente():
    instancia_demanda_model = Demanda_model()
    resposta = instancia_demanda_model.ler_com_filtro_status(1)
    assert type(resposta) == list
    assert len(resposta) > 0, "Nenhum resgistro com status 1 encontrado"
    for registro in resposta:
        assert registro.dem_status == 1

def test_buscar_demandas_por_local_retorna_corretamente():
    instancia_demanda_model = Demanda_model()
    resposta = instancia_demanda_model.ler_com_filtro_local("SMECICT")
    assert type(resposta) == list
    assert len(resposta) > 0, "Nenhum resgistro com status 1 encontrado"
    for registro in resposta:
        assert registro.dem_local == "SMECICT"

def test_buscar_demandas_por_prioridade_retorna_corretamente():
    instancia_demanda_model = Demanda_model()
    resposta = instancia_demanda_model.ler_com_filtro_prioridade(0)
    assert type(resposta) == list
    assert len(resposta) > 0, "Nenhum resgistro com status 1 encontrado"
    for registro in resposta:
        assert registro.dem_prioridade == 0

def test_atualizar_retorna_true_com_dados_corretos():
    instancia_demanda_model = Demanda_model()
    instancia = construct_model(instancia_demanda_model, 1)
    resposta = instancia.atualizar(protocolo=1234567890, dem_descricao="test")
    assert resposta['atualizado'] == True

def test_atualizar_retorna_false_com_dados_incorretos():
    instancia_demanda_model = Demanda_model()
    instancia = construct_model(instancia_demanda_model, 1)
    resposta = instancia.atualizar(protocolo=0, dem_descricao=929)
    assert resposta['atualizado'] == False

def test_remover_registro_por_protocolo_funciona():
    mock_protocolo = 1234567890
    instancia_demanda_model = Demanda_model()
    resposta = instancia_demanda_model.remover(mock_protocolo)
    assert resposta['removido'] == True

