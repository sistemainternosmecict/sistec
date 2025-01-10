from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import logging, os

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

class NiveisAcesso_model(Base):
    __tablename__ = 'tb_niveis_acesso'

    nva_id = Column(Integer, primary_key=True, autoincrement=True)
    nva_nome = Column(String(50), nullable=False, unique=True)
    nva_desc = Column(String(255), nullable=True)

    def __init__(self, dados: dict = None):
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        # self.engine = create_engine('sqlite:///nvlacesso.db', echo=True)
        self.engine = create_engine(db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
        if dados:
            self.distribuir_dados(dados)

    def __repr__(self):
        return f"<NiveisAcesso(nva_id={self.nva_id}, nva_nome={self.nva_nome}, nva_desc={self.nva_desc})>"

    def distribuir_dados(self, dados: dict) -> None:
        if 'nva_nome' in dados:
            self.nva_nome = dados['nva_nome']
        if 'nva_desc' in dados:
            self.nva_desc = dados['nva_desc']

    def registrar_novo_nivel(self) -> dict:
        nivel_existente = self.session.query(NiveisAcesso_model).filter_by(nva_nome=self.nva_nome).first()
        if nivel_existente:
            return {"msg": f"O nível de acesso '{self.nva_nome}' já está cadastrado. Por favor, use outro nome!", "registro": False}
        
        try:
            self.session.add(self)
            self.session.commit()
            return {"msg": "Registro realizado!", "registro": True, "id": self.nva_id}
        except Exception as e:
            self.session.rollback()
            return {"msg": f"Erro ao registrar: {str(e)}", "registro": False}

    def ler_todos_os_niveis(self) -> dict:
        return {'todos_niveis': self.session.query(NiveisAcesso_model).all()}

    def ler_pelo_id(self, id: int) -> dict:
        nivel = self.session.query(NiveisAcesso_model).filter_by(nva_id=id).first()
        return {'nivel': nivel}

    def ler_pelo_nome(self, nome: str) -> dict:
        nivel = self.session.query(NiveisAcesso_model).filter_by(nva_nome=nome).first()
        return {'nivel': nivel}

    def atualizar_nivel(self, **kwargs) -> dict:
        modificado = []
        id = kwargs.get('nva_id')
        nivel = self.ler_pelo_id(id)
        if nivel['nivel'] and len(kwargs) > 1:
            for key, value in kwargs.items():
                if key != 'nva_id':
                    setattr(nivel['nivel'], key, value)
                    modificado.append(key)
            try:
                self.session.commit()
                return {'atualizado': True, 'modificado': modificado}
            except Exception as e:
                self.session.rollback()
                return {'atualizado': False, 'msg': f"Erro ao atualizar: {str(e)}"}
        return {'atualizado': False}

    def remover_nivel(self, nva_id) -> dict:
        nivel = self.session.query(NiveisAcesso_model).filter(NiveisAcesso_model.nva_id == nva_id).first()
        if nivel:
            try:
                self.session.delete(nivel)
                self.session.commit()
                return {'removido': True}
            except Exception as e:
                self.session.rollback()
                return {'removido': False, 'msg': f"Erro ao remover: {str(e)}"}
        return {'removido': False, 'msg': "Nível de acesso não encontrado."}
