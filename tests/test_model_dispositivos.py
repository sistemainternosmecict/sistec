import pytest
from models.dispositivos import Dispositivo_model

@pytest.fixture
def dispositivo_data():
    return {
        "disp_id":1,
        "disp_serial": "ABC123456789",
        "disp_tipo": 1,
        "disp_desc": "Dispositivo de teste"
    }

def test_create_dispositivo(dispositivo_data):
    dispositivo = Dispositivo_model()
    novo_dispositivo = dispositivo.create_dispositivo(
        dispositivo_data["disp_serial"], 
        dispositivo_data["disp_tipo"], 
        dispositivo_data["disp_desc"]
    )
    
    assert novo_dispositivo.disp_id is not None
    assert novo_dispositivo.disp_serial == dispositivo_data["disp_serial"]
    assert novo_dispositivo.disp_tipo == dispositivo_data["disp_tipo"]
    assert novo_dispositivo.disp_desc == dispositivo_data["disp_desc"]

def test_update_dispositivo(dispositivo_data):
    dispositivo = Dispositivo_model()

    dispositivo_atualizado = dispositivo.update_dispositivo(
        dispositivo_data["disp_id"], 
        disp_desc="Descrição atualizada"
    )
    
    assert dispositivo_atualizado is not None
    assert dispositivo_atualizado.disp_desc == "Descrição atualizada"

def test_get_all_dispositivos(dispositivo_data):
    dispositivo = Dispositivo_model()
    
    dispositivos = dispositivo.get_all_dispositivos()
    assert len(dispositivos) > 0
    assert dispositivos[0].disp_serial == dispositivo_data["disp_serial"]

def test_get_dispositivo_by_serial(dispositivo_data):
    dispositivo = Dispositivo_model()
    
    dispositivo_obtido = dispositivo.get_dispositivo_by_serial(dispositivo_data["disp_serial"])
    assert dispositivo_obtido is not None
    assert dispositivo_obtido.disp_serial == dispositivo_data["disp_serial"]

def test_delete_dispositivo(dispositivo_data):
    dispositivo = Dispositivo_model()

    resultado = dispositivo.delete_dispositivo(dispositivo_data["disp_id"])
    assert resultado is True
    
    dispositivo_excluido = dispositivo.get_dispositivo_by_serial(dispositivo_data["disp_serial"])
    assert dispositivo_excluido is None
