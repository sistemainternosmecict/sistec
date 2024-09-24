from modules.demandas import Gerenciador_demandas #, Demanda
# from models.demandas import Demanda_model

def test_gerenciador_demandas_instancianda():
    instancia_gerenciador = Gerenciador_demandas()
    assert isinstance(instancia_gerenciador, Gerenciador_demandas)

def test_gerenciador_demandas_carregando_tudo():
    instancia_gerenciador = Gerenciador_demandas()
    resultado = instancia_gerenciador.obter_demandas()
    assert resultado != []

def test_gerenciador_demandas_criar_nova_demanda():
    mock_dados = {
        "nvl_prioridade":0,
        "direcionamento":1,
        "solicitante":1,
        "descricao":"PC ficou ruim",
        "tipo":1,
        "local":"SMECICT",
        "sala":"15b"
    }
    instancia_gerenciador = Gerenciador_demandas()
    demanda = instancia_gerenciador.criar_nova_demanda(mock_dados)
    assert type(demanda) == dict
    assert demanda['inserido'] == True

def test_gerenciador_demandas_agregar_demanda():
    mock_dados = {
        "nvl_prioridade":0,
        "direcionamento":2,
        "solicitante":3,
        "descricao":"Chrome ficou ruim",
        "tipo":1,
        "local":"SMECICT",
        "sala":"15b"
    }
    instancia_gerenciador = Gerenciador_demandas()
    instancia_gerenciador.criar_nova_demanda(mock_dados)
    resultado = instancia_gerenciador.obter_demandas()
    assert len(resultado) > 0

def test_gerenciador_demandas_agregar_demanda():
    mock_dados = {
        "nvl_prioridade":0,
        "direcionamento":1,
        "solicitante":1,
        "descricao":"PC ficou ruim",
        "tipo":1,
        "local":"SMECICT",
        "sala":"15b"
    }
    instancia_gerenciador = Gerenciador_demandas()
    demanda = instancia_gerenciador.criar_nova_demanda(mock_dados)
    resultado = instancia_gerenciador.agregar_demanda(demanda)
    assert 'agregada' in resultado
    assert resultado['agregada'] == True

def test_gerenciador_demandas_carregar_todas_as_demandas_funciona():
    instancia_gerenciador = Gerenciador_demandas()
    instancia_gerenciador.carregar_todas_as_demandas()
    demandas = instancia_gerenciador.obter_demandas()
    assert len(demandas) > 3
