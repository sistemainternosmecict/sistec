from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

# Construir a URL do banco de dados usando as variáveis de ambiente
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
Base = declarative_base()

class Notificacao_model(Base):
    __tablename__ = "tb_notificacoes"
    
    not_id = Column(Integer, primary_key=True, autoincrement=True)
    not_message = Column(String(100), nullable=False)
    not_data = Column(String(10), nullable=False)
    not_hora = Column(String(8), nullable=False)
    not_lida = Column(Boolean, default=False)
    not_protocolo = Column(BigInteger)
    
    def __init__(self):
        self.engine = create_engine(db_url, echo=True, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
    
    def __repr__(self):
        return f"""<Notificacao(not_id={self.not_id}, 
            not_message={self.not_message}, 
            not_data={self.not_data}, 
            not_hora={self.not_hora}, 
            not_lida={self.not_lida},
            not_protocolo={self.not_protocolo})>"""
    
    def create(self, not_message:str, not_data:str, not_hora:str, not_protocolo, not_lida:bool=False):
        self.not_message=not_message
        self.not_data=not_data
        self.not_hora=not_hora
        self.not_lida=not_lida
        self.not_protocolo=not_protocolo
        self.session.add(self)
        self.session.commit()
        return self

    def read(self, not_id:int):
        return self.session.query(Notificacao_model).filter(Notificacao_model.not_id==not_id).first()
    
    def get_all(self):
        return self.session.query(Notificacao_model).all()

    def update(self, not_id:int, **kwargs):
        notificacao = self.session.query(Notificacao_model).filter(Notificacao_model.not_id==not_id).first()
        if notificacao:
            for key, value in kwargs.items():
                setattr(notificacao, key, value)
            self.session.commit()
        return notificacao

    def delete(self, not_id):
        notificacao = self.session.query(Notificacao_model).filter(Notificacao_model.not_id==not_id).first()
        if notificacao:
            self.session.delete(notificacao)
            self.session.commit()
        return notificacao