from modules.usuarios import Gerenciador_usuarios, Solicitante, Colaborador
from models.solicitantes import Solicitante_model
from models.colaboradores import Colaborador_model

def test_gerenciador_usuarios_verificar_campos_vazio_retornar_4_campos():
    gerenciador = Gerenciador_usuarios()

    dict_test = {}
    campos = gerenciador.verificar_campos(dict_test)

    esperado = 4
    comprimento = len(campos)

    assert comprimento == esperado

def test_gerenciador_usuarios_construir_solicitante_retorna_obj():
    gerenciador = Gerenciador_usuarios()
    dict_test = {
        "usuario_nome":"Thyéz",
        "usuario_sala":"24",
        "usuario_email":"mail1@mail.com",
        "usuario_telefone":"22900000000"
    }
    campos = gerenciador.verificar_campos(dict_test)
    if len(campos) == 0:
        resultado = gerenciador.construir_solicitante(dict_test)
        assert type(resultado) == Solicitante

def test_gerenciador_usuarios_construir_colaborador_retorna_obj():
    gerenciador = Gerenciador_usuarios()
    dict_test = {
        "usuario_nome":"Thyéz",
        "usuario_sala":"24",
        "usuario_email":"mail2@mail.com",
        "usuario_telefone":"22900000000"
    }
    campos = gerenciador.verificar_campos(dict_test)
    if len(campos) == 0:
        resultado = gerenciador.construir_colaborador(dict_test)
        assert type(resultado) == Colaborador

def test_gerenciador_usuarios_registrar_solicitante():
    gerenciador = Gerenciador_usuarios()
    dict_test = {
        "usuario_nome":"Thyéz",
        "usuario_sala":"24",
        "usuario_email":"mail3@mail.com",
        "usuario_telefone":"22900000000"
    }
    resultado = gerenciador.registrar_solicitante(dict_test)
    assert resultado['res']['registro'] == True
    
def test_gerenciador_usuarios_carregar_solicitante_via_id_retorna_solicitante():
    gerenciador = Gerenciador_usuarios()
    resultado2 = gerenciador.carregar_solicitante_via_id(1)
    assert type(resultado2['obj']) == Solicitante_model

def test_gerenciador_usuarios_remover_solicitante():
    gerenciador = Gerenciador_usuarios()
    resultado = gerenciador.remover_solicitante_via_id(1)
    assert resultado['removido'] == True

def test_gerenciador_usuarios_registrar_colaborador():
    gerenciador = Gerenciador_usuarios()
    dict_test = {
        "usuario_nome":"Thyéz",
        "usuario_sala":"24",
        "usuario_email":"mail@mail.com",
        "usuario_telefone":"22900000000",
        "colab_nome_usuario":"thyez_s24",
        "colab_senha":"senhateste"
    }
    resultado = gerenciador.registrar_colaborador(dict_test)
    assert resultado['res']['registro'] == True

def test_gerenciador_usuarios_carregar_colaborador_via_id_retorna_colaborador():
    gerenciador = Gerenciador_usuarios()
    resultado2 = gerenciador.carregar_colaborador_via_id(1)
    assert type(resultado2['obj']) == Colaborador_model