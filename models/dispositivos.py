from sqlalchemy import Column, Integer, String, Boolean, create_engine
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

class Dispositivo_model(Base):
    __tablename__ = 'tb_dispositivos'

    disp_id = Column(Integer, primary_key=True, autoincrement=True)
    disp_serial = Column(String(30))
    disp_tipo = Column(Integer)
    disp_desc = Column(String(300))

    def __init__(self):
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url, echo=True, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def create_dispositivo(self, disp_serial, disp_tipo, disp_desc):
        novo_dispositivo = Dispositivo_model()
        novo_dispositivo.disp_serial = disp_serial
        novo_dispositivo.disp_tipo = disp_tipo
        novo_dispositivo.disp_desc = disp_desc
        self.session.add(novo_dispositivo)
        self.session.commit()
        return novo_dispositivo

    def update_dispositivo(self, disp_id, disp_serial=None, disp_tipo=None, disp_desc=None):
        dispositivo = self.session.query(Dispositivo_model).filter_by(disp_id=disp_id).first()
        if not dispositivo:
            return None
        if disp_serial:
            dispositivo.disp_serial = disp_serial
        if disp_tipo is not None:
            dispositivo.disp_tipo = disp_tipo
        if disp_desc:
            dispositivo.disp_desc = disp_desc
        self.session.commit()
        return dispositivo

    def get_all_dispositivos(self):
        return self.session.query(Dispositivo_model).all()

    def get_dispositivo_by_serial(self, disp_serial):
        return self.session.query(Dispositivo_model).filter_by(disp_serial=disp_serial).first()

    def delete_dispositivo(self, disp_id):
        dispositivo = self.session.query(Dispositivo_model).filter(Dispositivo_model.disp_id == disp_id).first()
        if not dispositivo:
            return None
        self.session.delete(dispositivo)
        self.session.commit()
        return True

    def __repr__(self):
        return f"<Dispositivo(disp_id={self.disp_id}, disp_serial={self.disp_serial}, disp_tipo={self.disp_tipo}, disp_desc={self.disp_desc})>"
