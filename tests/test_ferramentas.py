from modules.utilidades.ferramentas import Ferramentas, Mensageiro


def test_ferramentas_instanciando():
    instancia_ferramentas = Ferramentas()
    assert isinstance(instancia_ferramentas, Ferramentas)

def test_ferramentas_gera_protocolo_retorna_corretamente():
    mock_de_id_de_demanda:str = 2024
    instancia_ferramentas = Ferramentas()
    resultado = instancia_ferramentas.gerar_protocolo(mock_de_id_de_demanda)
    assert type(resultado) == int

def test_ferramentas_encripta_senha_corretamente():
    mock_senha:str = "mock_de_senha"
    instancia_ferramentas = Ferramentas()
    resultado = instancia_ferramentas.encriptar_senha(mock_senha)
    assert type(resultado) == str

def test_ferramentas_data_hoje_retorna_certo():
    instancia_ferramentas = Ferramentas()
    resultado = instancia_ferramentas.obter_data_hoje()
    assert "data_hora" in resultado

def test_ferramentas_criar_mensageiro_retorna_mensageiro():
    instancia_ferramentas = Ferramentas()
    mensageiro = instancia_ferramentas.criar_mensageiro()
    assert type(mensageiro) == Mensageiro

def test_ferramentas_enviar_mensagem():
    dados = {
        "remetente":"remetenteteste",
        "destinatario":"alvo@mail.com",
        "assunto":"testedemensagem",
        "mensagem":"mensagemdeteste"
    }
    instancia_ferramentas = Ferramentas()
    instancia_ferramentas.criar_mensageiro()
    resposta = instancia_ferramentas.enviar_mensagem(dados)
    assert 'email_enviado' in resposta
    assert resposta['email_enviado'] == True

def test_ferramentas_enviar_mensagem_sem_dados_nao_funciona():
    dados = {}
    instancia_ferramentas = Ferramentas()
    instancia_ferramentas.criar_mensageiro()
    resposta = instancia_ferramentas.enviar_mensagem(dados)
    assert 'email_enviado' in resposta
    assert resposta['email_enviado'] == False
