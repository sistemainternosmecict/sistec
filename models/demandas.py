from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

# Construir a URL do banco de dados usando as variáveis de ambiente
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

Base = declarative_base()

class Demanda_model(Base):
    __tablename__ = 'tb_demandas'

    dem_protocolo = Column(BigInteger, primary_key=True, nullable=False)
    dem_solicitante_id = Column(Integer)
    dem_direcionamento_id = Column(Integer)
    dem_dt_entrada = Column(String(20))
    dem_dt_atendimento = Column(String(20))
    dem_tipo_demanda = Column(Integer)
    dem_local = Column(String(80))
    dem_sala = Column(String(30))
    dem_descricao = Column(String(300))
    dem_status = Column(Integer)
    dem_prioridade = Column(Integer)
    dem_dt_final = Column(String(20))
    dem_atendido_por_id = Column(Integer)
    dem_tempo_finalizacao = Column(Integer)
    dem_observacoes = Column(String(300))
    dem_link_oficio = Column(String(200))

    def __init__(self):
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url, echo=True)
        # self.engine = create_engine('sqlite:///demandas.db', echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
    
    def __repr__(self):
        return f"""<Demanda(dem_protocolo={self.dem_protocolo}, 
            dem_solicitante_id={self.dem_solicitante_id}, 
            dem_direcionamento_id={self.dem_direcionamento_id}, 
            dem_dt_entrada={self.dem_dt_entrada}, 
            dem_dt_atendimento={self.dem_dt_atendimento}, 
            dem_tipo_demanda={self.dem_tipo_demanda}, 
            dem_local={self.dem_local}, 
            dem_sala={self.dem_sala}, 
            dem_descricao={self.dem_descricao}, 
            dem_status={self.dem_status}, 
            dem_prioridade={self.dem_prioridade}, 
            dem_dt_final={self.dem_dt_final}, 
            dem_atendido_por_id={self.dem_atendido_por_id}, 
            dem_tempo_finalizacao={self.dem_tempo_finalizacao}, 
            dem_observacoes={self.dem_observacoes}, 
            dem_link_oficio={self.dem_link_oficio})>"""

    def ler_todos(self):
        return self.session.query(Demanda_model).all()

    def ler_pelo_protocolo(self, protocolo):
        return self.session.query(Demanda_model).filter_by(dem_protocolo=protocolo).first()

    def ler_com_filtro_status(self, status):
        return self.session.query(Demanda_model).filter_by(dem_status=status).all()

    def ler_com_filtro_local(self, local):
        return self.session.query(Demanda_model).filter_by(dem_local=local).all()

    def ler_com_filtro_prioridade(self, prioridade):
        return self.session.query(Demanda_model).filter_by(dem_prioridade=prioridade).all()

    def inserir(self):
        try:
            self.session.add(self)
            self.session.commit()
            return {'inserido':True, 'protocolo':self.dem_protocolo}
        except Exception as e:
            print(e)
        return {'inserido':False}

    def remover(self, protocolo):
        demanda = self.ler_pelo_protocolo(protocolo)
        if demanda:
            self.session.delete(demanda)
            self.session.commit()
            return {'removido':True}

    def atualizar(self, **kwargs):
        modificado = []
        protocolo = kwargs.get('protocolo')
        demanda = self.ler_pelo_protocolo(protocolo)
        if demanda and len(kwargs) > 1:
            for key, value in kwargs.items():
                setattr(demanda, key, value)
                modificado.append(key)
            self.session.commit()
            return {'atualizado':True, 'modificado':modificado}
        return {'atualizado':False}
