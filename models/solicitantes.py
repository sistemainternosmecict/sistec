from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Solicitante_model(Base):
    __tablename__ = 'tb_solicitantes'

    solic_id = Column(Integer, primary_key=True, autoincrement=True)
    solic_nome = Column(String(15), nullable=False)
    solic_sala = Column(String(4), nullable=False)
    solic_email = Column(String(100), unique=True, nullable=False)
    solic_telefone = Column(String(11))

    def __init__(self):
        self.engine = create_engine('sqlite:///solicitantes.db', echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def __repr__(self):
        return f"<Solicitante(solic_id={self.solic_id}, solic_nome={self.solic_nome}, solic_sala={self.solic_sala}, solic_email={self.solic_email}, solic_telefone={self.solic_telefone})>"

    # Operações CRUD

    def criar(self):
        try:
            self.session.add(self)
            self.session.commit()
            return { "msg":"Registro realizado!", "registro":True, "id":self.solic_id }
        except IntegrityError as e:
            self.session.rollback()
            if "UNIQUE constraint failed" in str(e):
                return { "msg":f"O email '{self.solic_email}' já está cadastrado. Por favor use outro email!", "registro":False }
            else:
                return { "msg":"Erro: Não foi possível criar o solicitante devido a um problema desconhecido!", "registro":False }

    def ler(self):
        resultado = self.session.query(Solicitante_model).filter_by(solic_id=self.solic_id).first()
        return resultado
    
    def ler_tudo(self):
        resultado = self.session.query(Solicitante_model).all()
        return resultado
    
    def verificar(self, solicitante_nome, solicitante_sala):
        if self.session.query(Solicitante_model).filter_by(solic_nome=solicitante_nome, solic_sala=solicitante_sala).first() != None:
            return True
        return False
    
    def atualizar(self, solic_nome=None, solic_sala=None, solic_email=None, solic_telefone=None):
        solicitante = self.session.query(Solicitante_model).filter_by(solic_id=self.solic_id).first()
        try:
            if solicitante:
                if solic_nome:
                    solicitante.solic_nome = solic_nome
                if solic_sala:
                    solicitante.solic_sala = solic_sala
                if solic_email:
                    solicitante.solic_email = solic_email
                if solic_telefone:
                    solicitante.solic_telefone = solic_telefone
                self.session.commit()
                return True
        except Exception as e:
            print(e)
        return False

    def deletar(self):
        solicitante = self.session.query(Solicitante_model).filter_by(solic_id=self.solic_id).first()
        if solicitante:
            try:
                self.session.delete(solicitante)
                self.session.commit()
                return True
            except Exception as e:
                print(e)
                return False