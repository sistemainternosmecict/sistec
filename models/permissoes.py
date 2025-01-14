from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import logging, os

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.pool').setLevel(logging.CRITICAL)

Base = declarative_base()

class Permissao_model(Base):
    __tablename__ = 'tb_permissao'
    
    perm_id = Column(Integer, primary_key=True, autoincrement=True)
    perm_nome = Column(String(50), nullable=False)
    perm_desc = Column(String(150), nullable=False)

    def __init__(self, dados: dict = None):
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url, echo=True, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
        if dados:
            self.distribuir_dados(dados)

    def __repr__(self):
        return f"<Permissao_model(perm_id={self.perm_id}, perm_nome='{self.perm_nome}', perm_desc='{self.perm_desc}')>"
    
    def distribuir_dados(self, dados: dict) -> None:
        if 'nva_nome' in dados:
            self.nva_nome = dados['nva_nome']
    
    # Método para criar uma nova permissão
    def registrar(self, dados:dict):
        self.perm_nome = dados['perm_nome']
        self.perm_desc = dados['perm_desc']
    
        perm_existente = self.session.query(Permissao_model).filter_by(perm_nome=self.perm_nome).first()
        if perm_existente:
            return {"msg": f"A permissao '{self.perm_nome}' já está cadastrada. Por favor, use outro nome!", "registro": False}
        
        try:
            self.session.add(self)
            self.session.commit()
            return {"msg": "Registro realizado!", "registro": True, "id": self.perm_id}
        except Exception as e:
            self.session.rollback()
            return {"msg": f"Erro ao registrar: {str(e)}", "registro": False}

    # Método para buscar uma permissão por ID
    def ler_por_id(self, perm_id:int):
        return self.session.query(Permissao_model).filter_by(perm_id=perm_id).first()

    def ler_todos(self):
        return self.session.query(Permissao_model).all()
    
    # Método para atualizar uma permissão
    def atualizar(self, **kwargs) -> dict:
        modificado = []
        perm_id = kwargs.get('perm_id')

        # Buscar a permissão pelo ID
        perm = self.session.query(Permissao_model).filter_by(perm_id=perm_id).first()

        if perm and len(kwargs) > 1:
            # Atualizar os atributos fornecidos
            for key, value in kwargs.items():
                if key != 'perm_id' and hasattr(perm, key):
                    setattr(perm, key, value)
                    modificado.append(key)

            try:
                self.session.commit()
                return {'atualizado': True, 'modificado': modificado}
            except Exception as e:
                self.session.rollback()
                return {'atualizado': False, 'msg': f"Erro ao atualizar: {str(e)}"}

        return {'atualizado': False, 'msg': 'Permissão não encontrada ou nenhum atributo para atualizar'}


    # Método para deletar uma permissão
    def remover_permissao(self, perm_id:int) -> dict:
        perm = self.session.query(Permissao_model).filter(Permissao_model.perm_id == perm_id).first()
        if perm:
            try:
                self.session.delete(perm)
                self.session.commit()
                return {'removido': True}
            except Exception as e:
                self.session.rollback()
                return {'removido': False, 'msg': f"Erro ao remover: {str(e)}"}
        return {'removido': False, 'msg': "Permissão não encontrada."}

