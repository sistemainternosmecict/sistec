import pytest
from datetime import datetime
from models.notificacoes import Notificacao_model

def test_create_notificacao():
    model = Notificacao_model()
    model.create("Nova notificação, teste", datetime.now().strftime("%d/%m/%Y"), datetime.now().strftime("%H:%M"), False)
    assert model.not_message == "Nova notificação, teste"

def test_read_notificacao():
    model = Notificacao_model()
    fetched = model.read(5)
    assert fetched is not None
    assert fetched.not_message == "Nova notificação, teste"

def test_all_notificacao():
    model = Notificacao_model()
    fetched = model.get_all()
    print(fetched)
    assert len(fetched) > 0

def test_update_notificacao():
    model = Notificacao_model()
    result = model.update(5, not_lida=True)
    print("update", result)
    assert result.not_lida == True

def test_delete_notificacao():
    model = Notificacao_model()
    model.delete(5)
    assert model.not_id is None
