import pytest
from modules.usuarios import Permissao, GerenciadorPermissoes
from models.permissoes import Permissao_model, Base
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

@pytest.fixture
def gerenciador_permissoes(test_db):
    # Configura um gerenciador com acesso ao banco de dados de teste
    return GerenciadorPermissoes()

# Teste para registrar uma permissão
def test_registrar_permissao(gerenciador_permissoes, permissao_data):
    resultado = gerenciador_permissoes.registrar_permissao(permissao_data)
    permissoes = gerenciador_permissoes.obter_permissoes()

    assert resultado["registro"] is True
    assert resultado["msg"] == "Registro realizado!"
    assert len(permissoes) == 1
    assert permissoes[0]['perm_nome'] == permissao_data['perm_nome']

# Teste para carregar permissões
def test_carregar_permissoes(test_db, permissao_data):
    # Registrar uma permissão
    model = Permissao_model()
    model.session = test_db
    model.registrar(permissao_data)

    # Verificar carregamento pelo gerenciador
    gerenciador = GerenciadorPermissoes()
    permissoes = gerenciador.obter_permissoes()
    assert len(permissoes) == 1
    assert permissoes[0]['perm_nome'] == permissao_data['perm_nome']
    assert permissoes[0]['perm_desc'] == permissao_data['perm_desc']

# Teste para buscar uma permissão por ID
def test_buscar_permissao(gerenciador_permissoes, permissao_data):
    gerenciador_permissoes.registrar_permissao(permissao_data)
    permissoes = gerenciador_permissoes.obter_permissoes()

    permissao = gerenciador_permissoes.buscar_permissao(permissoes[0]['perm_id'])
    assert permissao is not None
    assert permissao.perm_nome == permissao_data['perm_nome']

# Teste para atualizar uma permissão
def test_atualizar_permissao(gerenciador_permissoes, permissao_data):
    gerenciador_permissoes.registrar_permissao(permissao_data)
    novos_dados = {"perm_id": 1, "perm_desc": "Descrição atualizada"}
    resultado = gerenciador_permissoes.atualizar_permissao(novos_dados)

    assert resultado["atualizado"] is True
    assert "perm_desc" in resultado["modificado"]

    permissao_atualizada = gerenciador_permissoes.buscar_permissao(1)
    assert permissao_atualizada.perm_desc == "Descrição atualizada"

# # Teste para remover uma permissão
def test_remover_permissao(gerenciador_permissoes, permissao_data):
    gerenciador_permissoes.registrar_permissao(permissao_data)

    resultado = gerenciador_permissoes.remover_permissao(1)
    assert resultado["removido"] is True

# # Teste para tentar remover uma permissão inexistente
def test_remover_permissao_inexistente(gerenciador_permissoes):
    resultado = gerenciador_permissoes.remover_permissao(99)  # ID inexistente
    assert resultado is None
