from modules.demandas.gsheet import GSheetManager
from modules.demandas.autenticadorGDrive import Autenticador

def test_intanciando_normalmente():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    assert isinstance(GSHEET_MAN, GSheetManager)

def test_obtendo_lista_normalmente():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    dados = GSHEET_MAN.obter_dados()
    assert type(dados) == list

def test_insercao_normal():
    mock_dados = ["123456789", "0", "10/10/2024", "-", "Solicitante", "Teste", "Colaborador", "Local", "Sala", "[COD]Dispositivo -> incidente", "Nova demanda"]
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.inserir_dados(mock_dados)
    assert resultado == True

def test_insercao_nao_conclui_com_dados_em_formato_errado():
    mock_dados = "dados no formato errado"
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.inserir_dados(mock_dados)
    assert resultado == False

def test_definir_pagina():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.definir_pagina("entrada")
    assert resultado == True

def test_atualiza_status_normalmente():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.atualizar_status(1, "Novo status")
    assert resultado == True

def test_atualiza_status_nao_funciona_com_formato_nao_esperado():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.atualizar_status(1, True)
    assert resultado == False

def test_atualiza_local_normalmente():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.atualizar_local(1, "Novo local")
    assert resultado == True

def test_atualiza_local_nao_funciona_com_formato_nao_esperado():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.atualizar_local(1, {})
    assert resultado == False

def test_atualiza_prioridade_normalmente():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.atualizar_prioridade(1, "1")
    assert resultado == True

def test_atualiza_prioridade_nao_funciona_com_formato_nao_esperado():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.atualizar_prioridade(1, 1)
    assert resultado == False

def test_atualiza_direcionamento_normalmente():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.atualizar_direcionamento(1, "Colaborador2")
    assert resultado == True

def test_atualiza_direcionamento_nao_funciona_com_formato_nao_esperado():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.atualizar_direcionamento(1, 145)
    assert resultado == False

def test_atualiza_status_para_finalizado():
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.atualizar_status(1, "finalizada")
    assert resultado == True

def test_transferencia_dados_entre_abas_funciona_nova_para_demandas():
    mock_dados = ["123456789", "1", "10/10/2024", "-", "Solicitante", "Teste", "Colaborador2", "Novo local", "Sala", "[COD]Dispositivo -> incidente", "finalizada", "01/10/2024", "", "-9"]
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "entrada", AUTH.obter_cliente())
    resultado = GSHEET_MAN.transferir_dados_entre_abas(1, "demandas")
    assert 'transferido' in resultado
    assert resultado == {'transferido':True, 'demanda':mock_dados}

def test_transferencia_dados_entre_abas_funciona_demandas_para_finalizadas():
    mock_dados = ["123456789", "1", "10/10/2024", "-", "Solicitante", "Teste", "Colaborador2", "Novo local", "Sala", "[COD]Dispositivo -> incidente", "finalizada", "01/10/2024", "", "-9"]
    AUTH = Autenticador()
    GSHEET_MAN = GSheetManager("controle_demandas", "demandas", AUTH.obter_cliente())
    resultado = GSHEET_MAN.transferir_dados_entre_abas(28, "os_finalizadas")
    assert 'transferido' in resultado
    assert resultado == {'transferido':True, 'demanda':mock_dados}