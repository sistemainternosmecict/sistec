import pytest
from unittest.mock import MagicMock

# Supondo que NivelDeAcesso e NiveisAcesso_model estejam no módulo nivel_de_acesso
from modules.usuarios import NivelDeAcesso, NiveisAcesso_model

@pytest.fixture
def mock_model():
    """Mocka a classe NiveisAcesso_model."""
    mock = MagicMock(spec=NiveisAcesso_model)
    mock.registrar_novo_nivel.return_value = {"msg": "Registro realizado!", "registro": True, "id": 1}
    return mock

def test_instanciar_com_dados():
    """Testa a criação de uma instância de NivelDeAcesso com dados."""
    dados = {"nva_id": 1, "nva_nome": "Admin", "nva_desc": "Acesso completo"}
    nivel = NivelDeAcesso(dados)
    assert nivel.nva_id == 1
    assert nivel.nva_nome == "Admin"
    assert nivel.nva_desc == "Acesso completo"

def test_instanciar_sem_dados():
    """Testa a criação de uma instância de NivelDeAcesso sem dados."""
    nivel = NivelDeAcesso()
    assert not hasattr(nivel, "nva_id")
    assert not hasattr(nivel, "nva_nome")
    assert not hasattr(nivel, "nva_desc")

def test_registrar():
    """Testa o método registrar da classe NivelDeAcesso."""
    # Monkeypatch para substituir a classe NiveisAcesso_model pelo mock
    # monkeypatch.setattr("nivel_de_acesso.NiveisAcesso_model", lambda dados: mock_model)

    dados = {"nva_nome": "Admin", "nva_desc": "Acesso completo"}
    nivel = NivelDeAcesso(dados)
    resultado = nivel.registrar()

    # Verifica se registrar_novo_nivel foi chamado com os dados corretos
    # mock_model.registrar_novo_nivel.assert_called_once()
    assert resultado["registro"] is True
    assert resultado["msg"] == "Registro realizado!"

def test_registrar_nivel_existente(mock_model, monkeypatch):
    """Testa o registro de um nível de acesso que já existe."""
    # mock_model.registrar_novo_nivel.return_value = {
    #     "msg": "O nível de acesso 'Admin' já está cadastrado. Por favor, use outro nome!",
    #     "registro": False,
    # }
    # monkeypatch.setattr("nivel_de_acesso.NiveisAcesso_model", lambda dados: mock_model)

    dados = {"nva_nome": "Admin", "nva_desc": "Acesso completo"}
    nivel = NivelDeAcesso(dados)
    resultado = nivel.registrar()

    # Verifica se a mensagem e o resultado estão corretos
    assert resultado["registro"] is False
    assert resultado["msg"] == "O nível de acesso 'Admin' já está cadastrado. Por favor, use outro nome!"

def test_registrar_excecao(mock_model, monkeypatch):
    """Testa o caso em que ocorre uma exceção ao registrar."""
    # mock_model.registrar_novo_nivel.side_effect = Exception("Erro inesperado")
    # monkeypatch.setattr("nivel_de_acesso.NiveisAcesso_model", lambda dados: mock_model)

    dados = {"nva_nome": 23, "nva_desc": 42}
    nivel = NivelDeAcesso(dados)
    res = nivel.registrar()
    assert res['registro'] == False

def test_remover_nivel():
    nivel = NivelDeAcesso({"nva_id":1})
    res = nivel.remover()

    assert res['removido'] == True