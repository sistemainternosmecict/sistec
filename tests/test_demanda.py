from modules.demandas import Demanda
# from models.demandas import Demanda_model

def construct_model(modelClass:object) -> object:
    dados = {
        'protocolo':1234567890,
        'solicitante':1,
        'direcionamento':1,
        'tipo':1,
        'dt_entrada':'2024/09/10|12:00',
        'status':1,
        'nvl_prioridade':0,
        'local':"SMECICT",
        'sala':"24",
        'descricao':'Descricao de teste',
        'dt_final':0,
        'tempo_finalizacao':0,
        'atendido_por':"test"
    }
    model = modelClass(dados)
    return model

def test_demanda_instancianda():
    instancia_demanda = construct_model(Demanda)
    assert isinstance(instancia_demanda, Demanda)

def test_demanda_definir_np_funciona():
    instancia_demanda = construct_model(Demanda)
    instancia_demanda.definir_np(1)
    dados_obtidos = instancia_demanda.obter_dados()
    assert dados_obtidos['nvl_prioridade'] == 1

def test_demanda_definir_direcionamento_funciona():
    instancia_demanda = construct_model(Demanda)
    instancia_demanda.definir_direcionamento(1)
    dados_obtidos = instancia_demanda.obter_dados()
    assert dados_obtidos['direcionamento'] == 1

def test_demanda_definir_status():
    instancia_demanda = construct_model(Demanda)
    instancia_demanda.definir_status("nova")
    dados_obtidos = instancia_demanda.obter_dados()
    assert dados_obtidos['status'] == "nova"

def test_demanda_registrar_nova_demanda():
    instancia_demanda = construct_model(Demanda)
    resultado = instancia_demanda.registrar_nova_demanda()
    assert resultado['inserido'] == True

def test_demanda_atualizar_demanda():
    dados = {
        "dem_dt_atendimento":"2024/09/11|12:00",
        "protocolo":20240920101008
    }
    instancia_demanda = Demanda(dados)
    resultado = instancia_demanda.atualizar_demanda(dados)

    assert resultado['atualizado'] == True
    assert 'modificado' in resultado
    assert resultado['modificado'] == ['dem_dt_atendimento', 'protocolo']

def test_demanda_finalizar_demanda():
    dados = {
        "dem_status":5,
        "protocolo":20240920101008
    }
    instancia_demanda = Demanda(dados)
    resultado = instancia_demanda.finalizar_demanda(dados)
    assert resultado['atualizado'] == True
    assert 'modificado' in resultado
    assert resultado['modificado'] == ['dem_status', 'protocolo']