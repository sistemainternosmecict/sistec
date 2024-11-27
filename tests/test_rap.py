import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.rel_acesso_perm import Base, RelAcessoPermn_model  # Certifique-se de ajustar o caminho do modelo conforme necessário
from modules.usuarios import Rel_acesso_perm  # Ajuste o caminho conforme necessário

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
    return {"rap_acesso_id": 1, "rap_perm_id": 1}

@pytest.fixture
def modelo(db_session):
    model = RelAcessoPermn_model()
    model.session = db_session  # Substitui a sessão pelo mock
    return model

def test_registrar_com_dados_validos(db_session, dados_validos):
    rel = Rel_acesso_perm(dados_validos)
    RelAcessoPermn_model.Session = sessionmaker(bind=db_session.bind) 
    resultado = rel.registrar()

    assert resultado["registro"] is True
    assert resultado["msg"] == "Relacionamento de acesso e permissão registrado com sucesso!"
    registro = db_session.query(RelAcessoPermn_model).filter_by(
        rap_acesso_id=dados_validos["rap_acesso_id"],
        rap_perm_id=dados_validos["rap_perm_id"]
    ).first()
    assert registro is not None

def test_registrar_com_dados_invalidos(db_session):
    dados_invalidos = {"rap_acesso_id": "invalido", "rap_perm_id": None}
    rel = Rel_acesso_perm(dados_invalidos)
    RelAcessoPermn_model.Session = sessionmaker(bind=db_session.bind)  # Redireciona para o banco de testes

    resultado = rel.registrar()

    assert resultado["registro"] is False
    assert "registro" in resultado

def test_registrar_relacionamento_duplicado(db_session, dados_validos):
    # Tenta registrar um relacionamento duplicado
    rel = Rel_acesso_perm(dados_validos)
    RelAcessoPermn_model.Session = sessionmaker(bind=db_session.bind)  # Redireciona para o banco de testes

    # Registra o relacionamento uma vez
    rel.registrar()

    # Tenta registrar novamente
    resultado = rel.registrar()

    assert resultado["registro"] is False
    assert "Já existe um relacionamento" in resultado["msg"]

def test_remover_rel_acesso_perm_por_id_usando_classe(db_session, dados_validos):
    # Configura a instância para a remoção usando o ID obtido
    rel_remocao = Rel_acesso_perm({"rap_id": 1})
    resultado_remocao = rel_remocao.remover()

    # Verifica o resultado da remoção
    assert resultado_remocao["removido"] is True
    assert resultado_remocao["msg"] == "Relacionamento de acesso e permissão removido com sucesso!"

    # Verifica se o registro foi realmente removido do banco
    registro_removido = db_session.query(RelAcessoPermn_model).filter_by(rap_id=1).first()
    assert registro_removido is None

