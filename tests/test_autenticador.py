from modules.usuarios import Autenticador
from modules.usuarios import Colaborador

mock_dados_colab = {
    "usuario_nome":"thyéz",
    "usuario_sala":"24",
    "usuario_email":"thyezolaiveira@gmail.com",
    "usuario_telefone":"22998548514",
    "colab_id":1
}

def test_autenticador_instanciando():
        instancia_autenticador = Autenticador()
        assert isinstance(instancia_autenticador, Autenticador)

def test_autenticador_login_com_credenciais_corretas_autoriza():
        instancia_autenticador = Autenticador()
        instancia_colaborador = Colaborador(mock_dados_colab)
        resultado_registro = instancia_colaborador.registrar_colaborador("thyez_s24", "senhateste")
        if resultado_registro['registro'] == True:
            credenciais = ["thyez_s24", "senhateste"]
            resultado = instancia_autenticador.login(credenciais)
            instancia_colaborador.remover_colaborador()
            assert resultado['login'] == True

def test_autenticador_login_com_credenciais_vazias_nao_autoriza():
    instancia_autenticador = Autenticador()
    resultado = instancia_autenticador.login(['', ''])
    assert resultado['auth'] == False
    assert 'campos vazios' in resultado['msg']

def test_autenticador_login_com_nome_usuario_invalido_nao_autoriza():
    instancia_autenticador = Autenticador()
    resultado = instancia_autenticador.login(['testuser', ''])
    assert resultado['auth'] == False
    assert 'não existe' in resultado['msg']

def test_autenticador_login_com_senha_incorreta_nao_autoriza():
    instancia_autenticador = Autenticador()
    instancia_colaborador = Colaborador(mock_dados_colab)
    resultado_registro = instancia_colaborador.registrar_colaborador("thyez_s24", "senhateste")
    if resultado_registro['registro'] == True:
        credenciais = ["thyez_s24", "senhateste_errada"]
        resultado = instancia_autenticador.login(credenciais)
        instancia_colaborador.remover_colaborador()
        assert resultado['auth'] == False

def test_autenticador_logout_funciona():
    instancia_autenticador = Autenticador()
    resultado = instancia_autenticador.logout()
    assert resultado['logout'] == True
    