from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from ..modules.utilidades.ferramentas import Ferramentas

Base = declarative_base()

class Colaborador_model(Base):
    __tablename__ = 'tb_solicitantes'

    colab_id = Column(Integer, primary_key=True, autoincrement=True)
    colab_sala = Column(String(10), nullable=False)
    colab_nome = Column(String(15), nullable=False)
    colab_nome_usuario = Column(String(10), nullable=False)
    colab_email = Column(String(100), unique=True, nullable=False)
    colab_telefone = Column(String(11))
    colab_senha = Column(String(100), unique=True, nullable=False)
    colab_ativo = Column(Boolean)

    def __init__(self):
        self.engine = create_engine('sqlite:///colaboradores.db', echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def __repr__(self):
        return f"""
        <Colaborador(
            colab_id={self.colab_id},
            colab_sala={self.colab_sala},
            colab_nome={self.colab_nome},
            colab_nome_usuario={self.colab_nome_usuario},
            colab_email={self.colab_email},
            colab_telefone={self.colab_telefone},
            colab_senha={self.colab_senha},
            colab_ativo={self.colab_ativo}
        )>"""

    # Operações CRUD

    def criar(self) -> dict:
        try:
            self.session.add(self)
            self.session.commit()
            return { "msg":"Registro realizado!", "registro":True, "id":self.colab_id }
        except IntegrityError as e:
            self.session.rollback()
            if "UNIQUE constraint failed" in str(e):
                if "colab_email" in str(e):
                    return { "msg":f"O email '{self.colab_email}' já está cadastrado. Por favor use outro email!", "registro":False }
                if "colab_senha" in str(e):
                    return { "msg":f"A senha inserida já está cadastradq. Por favor use outra senha para este usuario!", "registro":False }
            else:
                return { "msg":"Erro: Não foi possível criar o colaborador devido a um problema desconhecido!", "registro":False }
            
    def let_tudo(self) -> list:
        return self.session.query(Colaborador_model).all()

    def ler(self) -> object:
        return self.session.query(Colaborador_model).filter_by(colab_id=self.colab_id).first()
    
    def login(self, nome_usuario, senha_hash) -> object:
        return self.session.query(Colaborador_model).filter_by(colab_nome_usuario=nome_usuario, colab_senha=senha_hash).first()
    
    def colab_existe(self, nome_usuario:str) -> bool:
        return self.session.query(Colaborador_model).filter_by(colab_nome_usuario=nome_usuario).first()
    
    def verificar(self, colaborador_nome_usuario, colaborador_sala_id) -> bool:
        try:
            if self.session.query(Colaborador_model).filter_by(colab_nome_usuario=colaborador_nome_usuario, colab_sala_id=colaborador_sala_id).first() != None:
                return True
        except Exception as e:
            print(e)
        return False
    
    def atualizar(self, colab_sala=None, colab_nome=None, colab_nome_usuario=None, colab_email=None, colab_telefone=None, colab_senha=None, colab_ativo=None) -> bool:
        ferramentas = Ferramentas()
        colaborador = self.session.query(Colaborador_model).filter_by(colab_id=self.colab_id).first()
        if colaborador:
            try:
                if colab_sala:
                    colaborador.colab_sala = colab_sala
                if colab_nome:
                    colaborador.colab_nome = colab_nome
                if colab_nome_usuario:
                    colaborador.colab_nome_usuario = colab_nome_usuario
                if colab_email:
                    colaborador.colab_email = colab_email
                if colab_telefone:
                    colaborador.colab_telefone = colab_telefone
                if colab_senha:
                    colaborador.colab_senha = ferramentas.encriptar_senha(colab_senha)
                if colab_ativo:
                    colaborador.colab_ativo = colab_ativo
                self.session.commit()
                return True
            except Exception as e:
                print(e)
            return False

    def deletar(self) -> bool:
        colaborador = self.session.query(Colaborador_model).filter_by(colab_id=self.colab_id).first()
        if colaborador:
            try:
                self.session.delete(colaborador)
                self.session.commit()
                return True
            except Exception as e:
                print(e)
                return False