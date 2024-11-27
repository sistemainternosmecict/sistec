import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.rel_acesso_perm import Base, RelAcessoPermn_model
from modules.usuarios import Gerenciador_rap

@pytest.fixture(scope="module")
def db_session():
    engine = create_engine("sqlite:///rel_acesso_perm.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    engine.dispose()

@pytest.fixture
def dados_relacoes():
    return [
        {"rap_acesso_id": 1, "rap_perm_id": 2},
        {"rap_acesso_id": 3, "rap_perm_id": 4}
    ]

@pytest.fixture
def setup_dados_no_banco(db_session, dados_relacoes):
    for dados in dados_relacoes:
        relacao = RelAcessoPermn_model(dados)
        db_session.add(relacao)
    db_session.commit()

### TESTES PARA O GERENCIADOR_RAP ###
def test_gerenciador_carregar_dados_vazio(db_session):
    RelAcessoPermn_model.Session = sessionmaker(bind=db_session.bind)
    gerenciador = Gerenciador_rap()
    assert len(gerenciador.listar_relacoes_acesso_perm()) == 0

def test_gerenciador_registrar_relacao(db_session):
    RelAcessoPermn_model.Session = sessionmaker(bind=db_session.bind)
    gerenciador = Gerenciador_rap()
    nova_relacao = {"rap_acesso_id": 5, "rap_perm_id": 6}
    resultado = gerenciador.registrar_relacao_acesso_perm(nova_relacao)
    assert resultado["registro"] is True
    assert resultado["msg"] == "Relacionamento de acesso e permissão registrado com sucesso!"

def test_gerenciador_carregar_dados(db_session):
    RelAcessoPermn_model.Session = sessionmaker(bind=db_session.bind)
    gerenciador = Gerenciador_rap()
    relacoes = gerenciador.listar_relacoes_acesso_perm()
    assert len(relacoes) == 1

def test_gerenciador_buscar_relacao(db_session):
    RelAcessoPermn_model.Session = sessionmaker(bind=db_session.bind)
    gerenciador = Gerenciador_rap()

    # Busca um relacionamento existente pelo ID
    relacao = gerenciador.buscar_relacao_acesso_perm(1)
    assert relacao is not None
    assert relacao.rap_acesso_id == 5
    assert relacao.rap_perm_id == 6

    # Busca um relacionamento inexistente
    relacao_inexistente = gerenciador.buscar_relacao_acesso_perm(999)
    assert relacao_inexistente is None

def test_gerenciador_remover_relacao(db_session):
    RelAcessoPermn_model.Session = sessionmaker(bind=db_session.bind)
    gerenciador = Gerenciador_rap()

    # Remove um relacionamento existente
    rap_id = 1
    resultado_remocao = gerenciador.remover_relacao_acesso_perm(rap_id)

    assert resultado_remocao is not None
    assert resultado_remocao["removido"] is True
    assert resultado_remocao["msg"] == "Relacionamento de acesso e permissão removido com sucesso!"

    # Verifica se a relação foi removida da lista
    relacoes = gerenciador.listar_relacoes_acesso_perm()
    assert all(rel["rap_id"] != rap_id for rel in relacoes)

    # Tenta remover um relacionamento inexistente
    resultado_remocao_inexistente = gerenciador.remover_relacao_acesso_perm(999)
    assert resultado_remocao_inexistente is None
