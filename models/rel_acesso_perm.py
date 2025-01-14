from sqlalchemy import Column, Integer, Boolean, create_engine
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

class RelAcessoPermn_model(Base):
    __tablename__ = 'tb_rel_acesso_perm'

    rap_id = Column(Integer, primary_key=True, autoincrement=True)
    rap_acesso_id = Column(Integer, nullable=False)
    rap_perm_id = Column(Integer, nullable=False)
    rap_ativo = Column(Boolean, default=True)

    def __init__(self, dados: dict = None):
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url, echo=True, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
        if dados:
            self.distribuir_dados(dados)

    def __repr__(self):
        return f"<RelAcessoPermn_model(rap_id={self.rap_id}, rap_acesso_id={self.rap_acesso_id}, rap_perm_id={self.rap_perm_id}, rap_ativo={self.rap_ativo})>"
    
    def distribuir_dados(self, dados: dict) -> None:
        if 'rap_acesso_id' in dados:
            self.rap_acesso_id = dados['rap_acesso_id']
        if 'rap_perm_id' in dados:
            self.rap_perm_id = dados['rap_perm_id']
        if 'rap_ativo' in dados:
            self.rap_ativo = dados['rap_ativo']
    
    def registrar_novo_rel_acesso_perm(self) -> dict:
        rel_existente = self.session.query(RelAcessoPermn_model).filter_by(rap_acesso_id=self.rap_acesso_id, rap_perm_id=self.rap_perm_id).first()
        if rel_existente:
            return {"msg": f"Já existe um relacionamento entre o acesso '{self.rap_acesso_id}' e a permissão '{self.rap_perm_id}'. Por favor, verifique!", "registro": False}
        
        try:
            self.session.add(self)
            self.session.commit()
            return {"msg": "Relacionamento de acesso e permissão registrado com sucesso!", "registro": True}
        except Exception as e:
            self.session.rollback()
            return {"msg": f"Erro ao registrar: {str(e)}", "registro": False}

    def atualizar(self, **kwargs) -> dict:
        modificado = []
        rap_id = kwargs.get('rap_id')

        # Buscar o relacionamento pelo ID
        rel = self.session.query(RelAcessoPermn_model).filter_by(rap_id=rap_id).first()

        if rel and len(kwargs) > 1:
            # Atualizar os atributos fornecidos
            for key, value in kwargs.items():
                if key != 'rap_id' and hasattr(rel, key):
                    setattr(rel, key, value)
                    modificado.append(key)

            try:
                self.session.commit()
                return {'atualizado': True, 'modificado': modificado}
            except Exception as e:
                self.session.rollback()
                return {'atualizado': False, 'msg': f"Erro ao atualizar: {str(e)}"}

        return {'atualizado': False, 'msg': 'Relacionamento não encontrado ou nenhum atributo para atualizar'}

    def ler_rel_acesso_perm_por_id(self, rap_id: int):
        rel_acesso_perm = self.session.query(RelAcessoPermn_model).filter_by(rap_id=rap_id).first()
        if rel_acesso_perm:
            return {"rel_acesso_perm": rel_acesso_perm, "encontrado": True}
        return {"msg": "Relacionamento de acesso e permissão não encontrado.", "encontrado": False}
    
    def ler_todos(self):
        return self.session.query(RelAcessoPermn_model).all()
    
    def remover_rel_acesso_perm(self, rap_id: int) -> dict:
        rel_acesso_perm = self.session.query(RelAcessoPermn_model).filter_by(rap_id=rap_id).first()
        if rel_acesso_perm:
            try:
                self.session.delete(rel_acesso_perm)
                self.session.commit()
                return {"msg": "Relacionamento de acesso e permissão removido com sucesso!", "removido": True}
            except Exception as e:
                self.session.rollback()
                return {"msg": f"Erro ao remover: {str(e)}", "removido": False}
        return {"msg": "Relacionamento de acesso e permissão não encontrado.", "removido": False}