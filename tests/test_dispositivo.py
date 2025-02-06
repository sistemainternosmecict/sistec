import pytest
from modules.dispositivos import Dispositivo

@pytest.fixture
def dados_dispositivo():
    return {
        "disp_serial": "12345",
        "disp_tipo": 1,
        "disp_desc": "Teste"
    }

@pytest.fixture
def dispositivo(dados_dispositivo):
    return Dispositivo(dados_dispositivo)

def test_criar_dispositivo(dispositivo):
    novo_dispositivo = dispositivo.criar_dispositivo()
    assert novo_dispositivo is not None
    assert novo_dispositivo.disp_serial == "12345"
    assert novo_dispositivo.disp_tipo == 1
    assert novo_dispositivo.disp_desc == "Teste"

def test_atualizar_dispositivo(dispositivo):
    novos_dados = {"disp_serial": "67890", "disp_tipo": 2, "disp_desc": "Teste atualizado"}
    dispositivo_atualizado = dispositivo.atualizar_dispositivo(4, novos_dados)
    assert dispositivo_atualizado is not None
    assert dispositivo_atualizado.disp_serial == "67890"
    assert dispositivo_atualizado.disp_tipo == 2
    assert dispositivo_atualizado.disp_desc == "Teste atualizado"

def test_obter_todos_dispositivos(dispositivo):
    dispositivos = dispositivo.obter_todos_dispositivos()
    assert isinstance(dispositivos, list)

def test_obter_dispositivo_por_serial(dispositivo):
    dispositivo_encontrado = dispositivo.obter_dispositivo_por_serial("67890")
    assert dispositivo_encontrado is not None
    assert dispositivo_encontrado.disp_serial == "67890"

def test_deletar_dispositivo(dispositivo):
    resultado = dispositivo.deletar_dispositivo(4)
    assert resultado is True
