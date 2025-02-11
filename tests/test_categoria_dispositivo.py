import pytest
from models.categorias_dispositivos import Categoria_dispositivo

@pytest.fixture
def dados_categoria():
    return {
        "cat_disp_nome":"Chromebook",
        "cat_disp_modelo":"Samsung Chrome OS",
        "cat_disp_tipo":"Chrome de professor",
        "cat_disp_desc":"Dispositivos devem ser acessados usando o email institucional."
    }

@pytest.fixture
def categoria_repo():
    return Categoria_dispositivo()

def test_create_categoria(categoria_repo, dados_categoria):
    result = categoria_repo.create_categoria(**dados_categoria)
    assert result["created"] is True
    assert result["new_category_id"] is not None

def test_get_categoria_by_id(categoria_repo):
    categoria = categoria_repo.get_categoria_by_id(4)
    assert categoria is not None
    assert categoria.cat_disp_nome == "Chromebook"

def test_get_all_categorias(categoria_repo):
    categorias = categoria_repo.get_all_categorias()
    assert len(categorias) > 0

def test_update_categoria(categoria_repo):
    update_result = categoria_repo.update_categoria(4, cat_disp_nome="Categoria Atualizada")
    assert update_result["updated"] is True
    categoria_atualizada = categoria_repo.get_categoria_by_id(4)
    assert categoria_atualizada.cat_disp_nome == "Categoria Atualizada"

def test_delete_categoria(categoria_repo):
    delete_result = categoria_repo.delete_categoria(5)
    assert delete_result is True
    assert categoria_repo.get_categoria_by_id(5) is None
