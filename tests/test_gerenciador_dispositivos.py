import pytest
from modules.dispositivos import GerenciadorDispositivos

@pytest.fixture
def dados_dispositivo():
    return {
        "disp_serial": "12345",
        "disp_tipo": 1,
        "disp_desc": "Teste"
    }

@pytest.fixture
def gerenciador():
    return GerenciadorDispositivos()

def test_registrar_dispositivo(gerenciador, dados_dispositivo):
    novo_dispositivo = gerenciador.registrar_dispositivo(dados_dispositivo)
    assert novo_dispositivo is not None

def test_buscar_dispositivo_por_serial(gerenciador):
    dispositivo_encontrado = gerenciador.buscar_dispositivo_por_serial("12345")
    assert dispositivo_encontrado is not None

def test_atualizar_dispositivo(gerenciador, dados_dispositivo):
    novos_dados = {"disp_serial": "12345", "disp_tipo": 3, "disp_desc": "Teste atualizado 2"}
    dispositivo_atualizado = gerenciador.atualizar_dispositivo(13, novos_dados)
    
    assert dispositivo_atualizado is not None


def test_listar_dispositivos(gerenciador):
    dispositivos = gerenciador.listar_dispositivos()
    assert isinstance(dispositivos, list)


def test_remover_dispositivo(gerenciador):
    resultado = gerenciador.remover_dispositivo(13)
    assert resultado is True
