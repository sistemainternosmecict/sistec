import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.rel_acesso_perm import Base, RelAcessoPermn_model

@pytest.fixture(scope="module")
def db_session():
    # Configura um banco de dados SQLite em memória para os testes
    engine = create_engine("sqlite:///rel_acesso_perm.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session  # Fornece a sessão para os testes

    session.close()
    engine.dispose()

@pytest.fixture
def dados_validos():
    return {"rap_acesso_id": 1, "rap_perm_id": 2}

def test_registrar_novo_rel_acesso_perm(db_session, dados_validos):
    # Testa o registro de um novo relacionamento
    rel = RelAcessoPermn_model(dados_validos)
    rel.session = db_session  # Substitui a sessão pelo mock
    resultado = rel.registrar_novo_rel_acesso_perm()

    assert resultado["registro"] is True
    assert resultado["msg"] == "Relacionamento de acesso e permissão registrado com sucesso!"

    # Verifica se o registro foi salvo no banco
    registro = db_session.query(RelAcessoPermn_model).filter_by(
        rap_acesso_id=dados_validos["rap_acesso_id"],
        rap_perm_id=dados_validos["rap_perm_id"]
    ).first()
    assert registro is not None

def test_registrar_rel_duplicado(db_session, dados_validos):
    # Tenta registrar um relacionamento duplicado
    rel = RelAcessoPermn_model(dados_validos)
    rel.session = db_session  # Substitui a sessão pelo mock
    resultado = rel.registrar_novo_rel_acesso_perm()

    assert resultado["registro"] is False
    assert "Já existe um relacionamento" in resultado["msg"]

def test_ler_rel_acesso_perm_por_id(db_session, dados_validos):
    # Testa a leitura de um relacionamento pelo ID
    rel = db_session.query(RelAcessoPermn_model).filter_by(
        rap_acesso_id=dados_validos["rap_acesso_id"],
        rap_perm_id=dados_validos["rap_perm_id"]
    ).first()

    modelo = RelAcessoPermn_model()
    modelo.session = db_session  # Substitui a sessão pelo mock
    resultado = modelo.ler_rel_acesso_perm_por_id(rel.rap_id)

    assert resultado["encontrado"] is True
    assert resultado["rel_acesso_perm"].rap_id == rel.rap_id

def test_ler_rel_nao_existente(db_session):
    # Testa a leitura de um relacionamento inexistente
    modelo = RelAcessoPermn_model()
    modelo.session = db_session  # Substitui a sessão pelo mock
    resultado = modelo.ler_rel_acesso_perm_por_id(999)

    assert resultado["encontrado"] is False
    assert resultado["msg"] == "Relacionamento de acesso e permissão não encontrado."

def test_remover_rel_acesso_perm(db_session, dados_validos):
    # Testa a remoção de um relacionamento
    rel = db_session.query(RelAcessoPermn_model).filter_by(
        rap_acesso_id=dados_validos["rap_acesso_id"],
        rap_perm_id=dados_validos["rap_perm_id"]
    ).first()

    modelo = RelAcessoPermn_model()
    modelo.session = db_session  # Substitui a sessão pelo mock
    resultado = modelo.remover_rel_acesso_perm(rel.rap_id)

    assert resultado["removido"] is True
    assert resultado["msg"] == "Relacionamento de acesso e permissão removido com sucesso!"

    # Verifica se o registro foi removido
    registro = db_session.query(RelAcessoPermn_model).filter_by(rap_id=rel.rap_id).first()
    assert registro is None

def test_remover_rel_nao_existente(db_session):
    # Testa a tentativa de remover um relacionamento inexistente
    modelo = RelAcessoPermn_model()
    modelo.session = db_session  # Substitui a sessão pelo mock
    resultado = modelo.remover_rel_acesso_perm(999)

    assert resultado["removido"] is False
    assert resultado["msg"] == "Relacionamento de acesso e permissão não encontrado."
