import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.niveis_acesso import NiveisAcesso_model, Base

# Configuração do banco de dados para testes
@pytest.fixture(scope="module")
def test_db():
    engine = create_engine('sqlite:///nvlacesso.db', echo=True)  # Banco de dados em memória
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def nivel_acesso_data():
    return {"nva_nome": "Admin", "nva_desc": "Nível de acesso administrativo"}

# Teste para criar um novo nível de acesso
def test_registrar_novo_nivel(test_db, nivel_acesso_data):
    nivel = NiveisAcesso_model()
    nivel.session = test_db  # Substituir a sessão pelo banco de dados de teste
    nivel.distribuir_dados(nivel_acesso_data)

    resultado = nivel.registrar_novo_nivel()
    assert resultado["registro"] is True
    assert resultado["msg"] == "Registro realizado!"
    assert resultado["id"] is not None

# Teste para evitar duplicação de nomes
def test_duplicar_nivel(test_db, nivel_acesso_data):
    nivel = NiveisAcesso_model()
    nivel.session = test_db
    nivel.distribuir_dados(nivel_acesso_data)
    nivel.registrar_novo_nivel()

    nivel_duplicado = NiveisAcesso_model()
    nivel_duplicado.session = test_db
    nivel_duplicado.distribuir_dados(nivel_acesso_data)

    resultado = nivel_duplicado.registrar_novo_nivel()
    assert resultado["registro"] is False
    assert "já está cadastrado" in resultado["msg"]

# Teste para leitura de todos os registros
def test_ler_todos_os_niveis(test_db, nivel_acesso_data):
    nivel = NiveisAcesso_model()
    nivel.session = test_db
    nivel.distribuir_dados(nivel_acesso_data)
    nivel.registrar_novo_nivel()

    resultado = nivel.ler_todos_os_niveis()
    assert len(resultado["todos_niveis"]) == 1
    assert resultado["todos_niveis"][0].nva_nome == nivel_acesso_data["nva_nome"]

# Teste para leitura por ID
def test_ler_pelo_id(test_db, nivel_acesso_data):
    nivel = NiveisAcesso_model()
    nivel.session = test_db

    resultado = nivel.ler_pelo_id(1)
    assert resultado["nivel"] is not None
    assert resultado["nivel"].nva_nome == nivel_acesso_data["nva_nome"]

# # Teste para atualização de um nível de acesso
def test_atualizar_nivel(test_db):
    nivel = NiveisAcesso_model()
    nivel.session = test_db

    novos_dados = {"nva_id": 1, "nva_desc": "Descrição atualizada"}
    resultado = nivel.atualizar_nivel(**novos_dados)

    assert resultado["atualizado"] is True
    assert "nva_desc" in resultado["modificado"]

    nivel_atualizado = nivel.ler_pelo_id(1)
    assert nivel_atualizado["nivel"].nva_desc == "Descrição atualizada"

# # Teste para remoção de um nível de acesso
def test_remover_nivel(test_db, nivel_acesso_data):
    nivel = NiveisAcesso_model()
    nivel.session = test_db
    # nivel.distribuir_dados(nivel_acesso_data)
    # registro = nivel.registrar_novo_nivel()

    resultado = nivel.remover_nivel(1)
    assert resultado["removido"] is True

    nivel_removido = nivel.ler_pelo_id(1)
    assert nivel_removido["nivel"] is None
