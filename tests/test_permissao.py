import pytest
from models.permissoes import Permissao_model, Base
from modules.usuarios import Permissao
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados para testes
@pytest.fixture(scope="module")
def test_db():
    engine = create_engine('sqlite:///test_permissoes.db', echo=True)  # Banco de dados de teste
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def permissao_data():
    return {"perm_nome": "Admin", "perm_desc": "Permissão administrativa"}

# Teste para registrar uma nova permissão
def test_registrar_permissao(test_db, permissao_data):
    permissao = Permissao(permissao_data)
    resultado = permissao.registrar()

    assert resultado["registro"] is True
    assert resultado["msg"] == "Registro realizado!"
    assert resultado["id"] is not None

# Teste para evitar duplicação de permissões
def test_duplicar_permissao(test_db, permissao_data):
    permissao = Permissao(permissao_data)
    permissao.registrar()

    permissao_duplicada = Permissao(permissao_data)
    resultado = permissao_duplicada.registrar()

    assert resultado["registro"] is False
    assert "já está cadastrada" in resultado["msg"]

# Teste para leitura por ID
def test_ler_por_id(test_db, permissao_data):
    permissao = Permissao(permissao_data)
    resultado_registro = permissao.registrar()

    permissao_lida = Permissao()
    permissao_lida = permissao_lida.ler_por_id(1)
    assert permissao_lida.perm_nome == permissao_data["perm_nome"]
    assert permissao_lida.perm_desc == permissao_data["perm_desc"]

# Teste para atualizar uma permissão
def test_atualizar_permissao(test_db, permissao_data):
    permissao = Permissao(permissao_data)
    resultado_registro = permissao.registrar()

    novos_dados = {"perm_id": 1, "perm_desc": "Descrição atualizada"}
    resultado_atualizacao = permissao.atualizar(novos_dados)

    assert resultado_atualizacao["atualizado"] is True
    assert "perm_desc" in resultado_atualizacao["modificado"]

    permissao_lida = Permissao()
    permissao_lida = permissao_lida.ler_por_id(1)
    assert permissao_lida.perm_desc == "Descrição atualizada"

# Teste para remover uma permissão
def test_remover_permissao(test_db, permissao_data):
    permissao = Permissao(permissao_data)
    resultado_registro = permissao.registrar()

    resultado_remocao = permissao.remover(1)
    assert resultado_remocao["removido"] is True

    permissao_lida = Permissao_model().ler_por_id(1)
    assert permissao_lida is None

# Teste para tentar remover uma permissão inexistente
def test_remover_permissao_inexistente(test_db):
    permissao = Permissao()
    resultado_remocao = permissao.remover(99)  # ID inexistente

    assert resultado_remocao["removido"] is False
    assert resultado_remocao["msg"] == "Permissão não encontrada."
