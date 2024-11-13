from models.usuarios import Usuario_model

def construct_model(com_id:bool=False) -> Usuario_model:
    model = Usuario_model()
    if com_id:
        model.usuario_id = 7

    model.usuario_cpf = 75074680115
    model.usuario_nome = "Thyéz de Oliveira Monteiro"
    model.usuario_matricula = 95062191
    model.usuario_setor = "TI"
    model.usuario_sala = "24"
    model.usuario_cargo = 0
    model.usuario_email = "thyezoliveiramonteiro@smec.saquarema.rj.gov.br"
    model.usuario_telefone = 22998548514
    model.usuario_senha = "root"
    model.usuario_tipo = 1
    model.usuario_ativo = True
    return model

def test_instanciacao_do_modelo():
    instancia = construct_model()
    assert type(instancia) == Usuario_model

def test_insercao_normal():
    instancia = construct_model()
    esperado = { "msg":"Registro realizado!", "registro":True, "id":instancia.usuario_id }
    resultado = instancia.registrar_novo_usuario()
    assert resultado == esperado

def test_insercao_nao_permite_matricula_repetida():
    instancia = construct_model()
    esperado = { "msg":f"A matrícula {instancia.usuario_matricula} já está cadastrada. Por favor, use outra matrícula!", "registro":False }
    resultado = instancia.registrar_novo_usuario()
    assert resultado == esperado

def test_insercao_com_erro_aleatorio():
    esperado = False
    instancia = construct_model()
    instancia.usuario_cpf = "297839218734918273987"
    resultado = instancia.registrar_novo_usuario()
    assert resultado['registro'] == esperado

def test_usuario_printa_repr():
    instancia = construct_model(True)
    assert repr(instancia) == f"""<Usuario(usuario_id={instancia.usuario_id}, 
        usuario_cpf=75074680115, 
        usuario_nome=Thyéz de Oliveira Monteiro, 
        usuario_matricula=95062191, 
        usuario_setor=TI, 
        usuario_sala=24, 
        usuario_cargo=0, 
        usuario_email=thyezoliveiramonteiro@smec.saquarema.rj.gov.br, 
        usuario_telefone=22998548514, 
        usuario_tipo=1, 
        usuario_ativo=True)>"""

def test_obter_todos_os_usuarios():
    instancia = construct_model(True)
    resultado = instancia.ler_todos_os_registros()
    assert type(resultado['todos_usuarios']) == list
    assert len(resultado['todos_usuarios']) > 0

def test_obter_por_id():
    instancia = construct_model(True)
    resultado = instancia.ler_pelo_id(instancia.usuario_id)
    assert type(resultado['usuario']) == Usuario_model
    assert resultado['usuario'].usuario_nome == instancia.usuario_nome

def test_obter_por_cpf():
    instancia = construct_model()
    resultado = instancia.ler_pelo_cpf(instancia.usuario_cpf)
    assert type(resultado['usuario']) == Usuario_model
    assert resultado['usuario'].usuario_nome == instancia.usuario_nome

def test_obter_por_matricula():
    instancia = construct_model()
    resultado = instancia.ler_pelo_matricula(instancia.usuario_matricula)
    assert type(resultado['usuario']) == Usuario_model
    assert resultado['usuario'].usuario_nome == instancia.usuario_nome

def test_obter_por_nome():
    instancia = construct_model()
    resultado = instancia.ler_pelo_nome(instancia.usuario_nome)
    assert type(resultado['usuario']) == Usuario_model
    assert resultado['usuario'].usuario_nome == instancia.usuario_nome

def test_atualizar_cpf():
    esperado = {'atualizado':True, 'modificado':['usuario_cpf']}
    instancia = construct_model(True)
    resultado = instancia.atualizar_usuario(usuario_id=instancia.usuario_id, usuario_cpf=101010101010)
    assert resultado == esperado

def test_atualizar_nome():
    esperado = {'atualizado':True, 'modificado':['usuario_nome']}
    instancia = construct_model(True)
    resultado = instancia.atualizar_usuario(usuario_id=instancia.usuario_id, usuario_nome='atualizado')
    assert resultado == esperado

def test_atualizar_matricula():
    esperado = {'atualizado':True, 'modificado':['usuario_matricula']}
    instancia = construct_model(True)
    resultado = instancia.atualizar_usuario(usuario_id=instancia.usuario_id, usuario_matricula=98765)
    assert resultado == esperado
    
def test_atualizar_setor():
    esperado = {'atualizado':True, 'modificado':['usuario_setor']}
    instancia = construct_model(True)
    resultado = instancia.atualizar_usuario(usuario_id=instancia.usuario_id, usuario_setor="Adm")
    assert resultado == esperado

def test_credenciais_verificadas():
    instancia = Usuario_model()
    resultado = instancia.verificar_credenciais(98765, "root")
    assert type(resultado) == dict
    assert resultado['usuario'] != None
    assert resultado['verificado'] == True

def test_remocao_de_usuario():
    esperado = {'removido':True}
    instancia = construct_model(True)
    resultado = instancia.remover_usuario(instancia.usuario_id)
    assert resultado == esperado