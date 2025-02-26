from sqlalchemy import Column, Integer, String, Boolean, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging, os
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.pool').setLevel(logging.CRITICAL)
Base = declarative_base()

class Sala_model(Base):
    __tablename__ = 'tb_uni_salas'

    id_unico_sala = Column(Integer, primary_key=True, autoincrement=True)
    numero_sala = Column(Integer)
    sala_andar = Column(Integer)
    largura_sala = Column(Float, nullable=False)
    comprimento_sala = Column(Float, nullable=False)
    qnt_entradas = Column(Integer)
    largura_porta = Column(Float)
    qnt_janelas = Column(Integer)
    qnt_tomadas = Column(Integer)
    internet = Column(Boolean)
    tipo_sala = Column(String(50), nullable=False)
    uni_id = Column(Integer, nullable=False)

    def __init__(self):
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url, echo=True, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def __repr__(self):
        return f"<Sala(id_unico_sala={self.id_unico_sala}, nome_sala='{self.nome_sala}', numero_sala='{self.numero_sala}')>"

    def criar_sala(self):
        # sala_existente = self.session.query(self.__class__).filter_by(numero_sala=self.numero_sala).first()
        
        # if sala_existente.numero_sala != None:
        #     return {"msg": "Sala com este número já existe!", "registro": False}
        
        self.session.add(self)
        self.session.commit()
        return {"msg": "Registro realizado!", "registro": True, "id_registrado": self.id_unico_sala}

    def buscar_por_id(self, id: int):
        sala = self.session.query(Sala_model).filter(Sala_model.id_unico_sala == id).first()
        if sala:
            return {'sala': sala, 'encontrado': True}
        return {'sala': None, 'encontrado': False}

    def buscar_por_uni_id(self, uni_id: int):
        salas = self.session.query(Sala_model).filter(Sala_model.uni_id == uni_id).all()
        if salas:
            return {'salas': salas, 'encontrado': True}
        return {'salas': None, 'encontrado': False}

    def ler_todas(self, ordem='id_unico_sala'):
        return self.session.query(Sala_model).order_by(getattr(Sala_model, ordem)).all()

    def atualizar_sala(self, updates: dict):
        sala = self.buscar_por_id(updates['id_unico_sala'])
        if sala['encontrado']:
            for key, value in updates.items():
                setattr(sala['sala'], key, value)
            self.session.commit()
            return {'atualizado': True}
        return {'atualizado': False}

    def remover_sala(self, sala):
        if sala:
            self.session.delete(sala)
            self.session.commit()
            return {"msg": "Registro removido!", "removido": True}
        return {"msg": "Registro não pode ser removido!", "removido": False}
