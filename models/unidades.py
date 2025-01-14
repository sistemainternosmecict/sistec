from sqlalchemy import Column, Integer, String, Boolean, create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import logging, os
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

# Construir a URL do banco de dados usando as variáveis de ambiente
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.pool').setLevel(logging.CRITICAL)
Base = declarative_base()

class Unidade_model(Base):
    __tablename__ = 'tb_unidades'

    uni_id = Column(Integer, primary_key=True, autoincrement=True)
    uni_cod_ue = Column(Integer, nullable=False)
    uni_designador_categoria = Column(String, nullable=True)
    uni_nome = Column(String, nullable=False)
    uni_cep = Column(Integer, nullable=False)
    uni_logradouro = Column(String)
    uni_numero_end = Column(Integer)
    uni_bairro = Column(String)
    uni_distrito = Column(Integer)
    uni_direcao = Column(String)
    uni_telefone_direcao = Column(String)
    uni_segmentos = Column(String)
    uni_listada = Column(Boolean, default=False)

    def __init__(self):
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url, echo=True, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def __repr__(self):
        return f"<Unidade(uni_id={self.uni_id}, uni_nome='{self.uni_nome}', uni_cod_ue={self.uni_cod_ue})>"

    def criar_unidade(self):
        self.session.add(self)
        self.session.commit()
        res = {"msg":"Registro realizado!", "registro":True, "id_registrado":self.uni_id}
        return res

    def buscar_por_id(self, id):
        unidade = self.session.query(Unidade_model).filter_by(uni_id = id).first()
        if unidade:
            return {'unidade':unidade, 'encontrado':True}
        return {'unidade':None, 'encontrado':False}

    def buscar_por_cod_ue(self, uni_cod_ue):
        return self.session.query(Unidade_model).filter(Unidade_model.uni_cod_ue == uni_cod_ue).first()

    def buscar_por_categoria(self, designador_categoria):
        return self.session.query(Unidade_model).filter(Unidade_model.uni_designador_categoria == designador_categoria).all()

    def ler_todos(self, ordem='uni_id'):
        if ordem == 'uni_cod_ue':
            return self.session.query(Unidade_model).order_by(Unidade_model.uni_cod_ue).all()
        elif ordem == 'uni_nome':
            return self.session.query(Unidade_model).order_by(Unidade_model.uni_nome).all()
        return self.session.query(Unidade_model).order_by(Unidade_model.uni_id).all()

    def atualizar_unidade(self, uni_id, **kwargs):
        unidade = self.buscar_por_id(uni_id)
        if unidade:
            for key, value in kwargs.items():
                setattr(unidade, key, value)
            self.session.commit()
        return unidade

    def remover_unidade(self) -> dict:
        print(self)
        res = { "msg":"Registro não pode ser removido!", "removido":False }
        if self.uni_id > 0:
            self.session.delete(self)
            self.session.flush()
            self.session.commit()
            res = { "msg":"Registro removido!", "removido":True }
        return res

    def ativar_unidade(self, uni_id):
        unidade = self.buscar_por_id(uni_id)
        if unidade:
            unidade.uni_listada = True
            self.session.commit()
        return unidade

    def desativar_unidade(self, uni_id):
        unidade = self.buscar_por_id(uni_id)
        if unidade:
            unidade.uni_listada = False
            self.session.commit()
        return unidade
