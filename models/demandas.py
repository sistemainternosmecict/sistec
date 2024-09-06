from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Demanda_model(Base):
    __tablename__ = 'tb_demandas'

    dem_protocolo = Column(Integer, primary_key=True, nullable=False)
    tb_solicitantes_id = Column(Integer)
    tb_colaboradores_id = Column(Integer)
    dem_dt_entrada = Column(String(20))
    dem_tipo_demanda = Column(Integer)
    dem_local = Column(String(20))
    dem_descricao = Column(String(100))
    dem_status = Column(Integer)
    dem_prioridade = Column(Integer)
    dem_dt_final = Column(String(20))
    dem_atendido_por = Column(String(15))
    dem_tempo_finalizacao = Column(Integer)
    dem_observacoes = Column(String(300))
    dem_link_oficio = Column(String(200))

    def __init__(self):
        self.engine = create_engine('sqlite:///demandas.db', echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
    
    def __repr__(self):
        return f"""
        <Demanda(
            dem_protocolo={self.dem_protocolo},
            tb_solicitantes_id={self.tb_solicitantes_id},
            tb_colaboradores_id={self.tb_colaboradores_id},
            dem_dt_entrada={self.dem_dt_entrada},
            dem_tipo_demanda={self.dem_tipo_demanda},
            dem_local={self.dem_local},
            dem_descricao={self.dem_descricao},
            dem_status={self.dem_status},
            dem_prioridade={self.dem_prioridade},
            dem_dt_final={self.dem_dt_final},
            dem_atendido_por={self.dem_atendido_por},
            dem_tempo_finalizacao={self.dem_tempo_finalizacao},
            dem_observacoes={self.dem_observacoes},
            dem_link_oficio={self.dem_link_oficio}
        )>"""

    def ler_todos(self):
        return self.session.query(Demanda_model).all()

    def ler_pelo_protocolo(self, protocolo):
        return self.session.query(Demanda_model).filter_by(dem_protocolo=protocolo).first()

    def ler_com_filtro_status(self, status):
        return self.session.query(Demanda_model).filter_by(dem_status=status).all()

    def ler_com_filtro_local(self, local):
        return self.session.query(Demanda_model).filter_by(dem_local=local).all()

    def ler_com_filtro_prioridade(self, prioridade):
        return self.session.query(Demanda_model).filter_by(dem_dt_final=prioridade).all()

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

    def atualizar(self, **kwargs):
        protocolo = kwargs.get('protocolo')
        demanda = self.ler_pelo_protocolo(protocolo)
        if demanda and len(kwargs) > 1:
            for key, value in kwargs.items():
                setattr(demanda, key, value)
            self.session.commit()
            return {'atualizado':True}
        return {'atualizado':False}
