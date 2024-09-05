from modules.demandas import Demanda
from models.demandas import Demanda_model

def test_demanda_instancianda():
    dados = {'protocolo':0}
    instancia_demanda = Demanda(dados)
    assert isinstance(instancia_demanda, Demanda)

# def test_demanda_definir_protocolo_funciona():
#     dados = {'protocolo':0}
#     instancia_demanda = Demanda(dados)
#     instancia_demanda.definir_protocolo(1)
#     dados_obtidos = instancia_demanda.obter_dados()
#     assert dados_obtidos['protocolo'] == 1

def test_demanda_definir_np_funciona():
    dados = {'nvl_prioridade':0, 'protocolo':0}
    instancia_demanda = Demanda(dados)
    instancia_demanda.definir_np(1)
    dados_obtidos = instancia_demanda.obter_dados()
    assert dados_obtidos['nvl_prioridade'] == 1

def test_demanda_definir_direcionamento_funciona():
    dados = {'direcionamento':0, 'protocolo':0}
    instancia_demanda = Demanda(dados)
    instancia_demanda.definir_direcionamento(1)
    dados_obtidos = instancia_demanda.obter_dados()
    assert dados_obtidos['direcionamento'] == 1

def test_demanda_definir_status():
    dados = {'status':0, 'protocolo':0}
    instancia_demanda = Demanda(dados)
    instancia_demanda.definir_status("nova")
    dados_obtidos = instancia_demanda.obter_dados()
    assert dados_obtidos['status'] == "nova"

def test_demanda_registrar_nova_demanda():
    dados = {
        "nvl_prioridade":0,
        "direcionamento":1,
        "solicitante":1,
        "descricao":"PC ficou ruim",
        "tipo":1,
        "local":"sala0"
    }
    instancia_demanda = Demanda(dados)
    resultado = instancia_demanda.registrar_nova_demanda()

    assert resultado['inserido'] == True

def test_demanda_atualizar_demanda():
    dados = {
        "dem_local":"Testando_atualização",
        "protocolo":20240905153240
    }
    instancia_demanda = Demanda(dados)
    resultado = instancia_demanda.atualizar_demanda(dados)

    assert resultado['atualizado'] == True

def test_demanda_finalizar_demanda():
    dados = {
        "status":5,
        "protocolo":20240905153240
    }
    instancia_demanda = Demanda(dados)
    resultado = instancia_demanda.finalizar_demanda(dados)
    assert resultado['atualizado'] == True