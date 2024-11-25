import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.permissoes import Permissao_model, Base

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
    permissao = Permissao_model()
    permissao.session = test_db
    resultado = permissao.registrar(permissao_data)

    assert resultado["registro"] is True
    assert resultado["msg"] == "Registro realizado!"
    assert resultado["id"] is not None

# Teste para evitar duplicação de permissões
def test_duplicar_permissao(test_db, permissao_data):
    permissao = Permissao_model()
    permissao.session = test_db
    permissao.registrar(permissao_data)

    permissao_duplicada = Permissao_model()
    permissao_duplicada.session = test_db
    resultado = permissao_duplicada.registrar(permissao_data)

    assert resultado["registro"] is False
    assert "já está cadastrada" in resultado["msg"]

# Teste para leitura de todas as permissões
def test_ler_todas_as_permissoes(test_db, permissao_data):
    permissao = Permissao_model()
    permissao.session = test_db
    permissao.registrar(permissao_data)

    resultado = permissao.ler_todos()
    assert len(resultado) == 1
    assert resultado[0].perm_nome == permissao_data["perm_nome"]

# Teste para leitura por ID
def test_ler_por_id(test_db, permissao_data):
    permissao = Permissao_model()
    permissao.session = test_db
    permissao.registrar(permissao_data)

    permissao_lida = permissao.ler_por_id(1)
    assert permissao_lida is not None
    assert permissao_lida.perm_nome == permissao_data["perm_nome"]

# Teste para atualizar uma permissão
def test_atualizar_permissao(test_db, permissao_data):
    permissao = Permissao_model()
    permissao.session = test_db
    permissao.registrar(permissao_data)

    novos_dados = {"perm_id": 1, "perm_desc": "Descrição atualizada"}
    resultado = permissao.atualizar(**novos_dados)

    assert resultado["atualizado"] is True
    assert "perm_desc" in resultado["modificado"]

    permissao_atualizada = permissao.ler_por_id(1)
    assert permissao_atualizada.perm_desc == "Descrição atualizada"

# Teste para remover uma permissão
def test_remover_permissao(test_db, permissao_data):
    permissao = Permissao_model()
    permissao.session = test_db
    permissao.registrar(permissao_data)

    resultado = permissao.remover_permissao(1)
    assert resultado["removido"] is True

    permissao_removida = permissao.ler_por_id(1)
    assert permissao_removida is None

# Teste para tentar remover uma permissão inexistente
def test_remover_permissao_inexistente(test_db):
    permissao = Permissao_model()
    permissao.session = test_db

    resultado = permissao.remover_permissao(99)  # ID inexistente
    assert resultado["removido"] is False
    assert resultado["msg"] == "Permissão não encontrada."
