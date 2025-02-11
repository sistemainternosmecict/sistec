from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging, os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.pool').setLevel(logging.CRITICAL)
Base = declarative_base()

class Categoria_dispositivo_model(Base):
    __tablename__ = 'tb_categorias_dispositivo'

    cat_disp_id = Column(Integer, primary_key=True, autoincrement=True)
    cat_disp_nome = Column(String(80))
    cat_disp_modelo = Column(String(200))
    cat_disp_tipo = Column(String(30))
    cat_disp_desc = Column(String(300))

    def __init__(self):
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url, echo=True, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def create_categoria(self, cat_disp_nome, cat_disp_modelo, cat_disp_tipo, cat_disp_desc):
        nova_categoria = Categoria_dispositivo_model()
        nova_categoria.cat_disp_nome = cat_disp_nome
        nova_categoria.cat_disp_modelo = cat_disp_modelo
        nova_categoria.cat_disp_tipo = cat_disp_tipo
        nova_categoria.cat_disp_desc = cat_disp_desc
        self.session.add(nova_categoria)
        self.session.commit()
        return {"created": True, "new_category_id": nova_categoria.cat_disp_id}

    def get_categoria_by_id(self, cat_disp_id:int):
        return self.session.query(Categoria_dispositivo_model).filter_by(cat_disp_id=cat_disp_id).first()

    def get_all_categorias(self):
        return self.session.query(Categoria_dispositivo_model).all()

    def update_categoria(self, cat_disp_id, cat_disp_nome=None, cat_disp_modelo=None, cat_disp_tipo=None, cat_disp_desc=None):
        categoria = self.session.query(Categoria_dispositivo_model).filter_by(cat_disp_id=cat_disp_id).first()
        if not categoria:
            return None
        if cat_disp_nome:
            categoria.cat_disp_nome = cat_disp_nome
        if cat_disp_modelo:
            categoria.cat_disp_modelo = cat_disp_modelo
        if cat_disp_tipo:
            categoria.cat_disp_tipo = cat_disp_tipo
        if cat_disp_desc:
            categoria.cat_disp_desc = cat_disp_desc
        self.session.commit()
        return {"updated": True}

    def delete_categoria(self, cat_disp_id):
        categoria = self.session.query(Categoria_dispositivo_model).filter(Categoria_dispositivo_model.cat_disp_id == cat_disp_id).first()
        if not categoria:
            return None
        self.session.delete(categoria)
        self.session.commit()
        return True

    def __repr__(self):
        return f"<Categoria_dispositivo_model(cat_disp_id={self.cat_disp_id}, cat_disp_nome={self.cat_disp_nome}, cat_disp_modelo={self.cat_disp_modelo}, cat_disp_tipo={self.cat_disp_tipo}, cat_disp_desc={self.cat_disp_desc})>"
