from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class RelAcessoPermn_model(Base):
    __tablename__ = 'tb_rel_acesso_perm'

    rap_id = Column(Integer, primary_key=True, autoincrement=True)
    rap_acesso_id = Column(Integer, nullable=False)
    rap_perm_id = Column(Integer, nullable=False)

    def __init__(self, dados: dict = None):
        # db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine('sqlite:///rel_acesso_perm.db', echo=True)
        # self.engine = create_engine(db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
        if dados:
            self.distribuir_dados(dados)

    def __repr__(self):
        return f"<RelAcessoPerm_model(rap_id={self.rap_id}, rap_acesso_id={self.rap_acesso_id}, rap_perm_id={self.rap_perm_id})>"
    
    def distribuir_dados(self, dados: dict) -> None:
        if 'rap_acesso_id' in dados:
            self.rap_acesso_id = dados['rap_acesso_id']
        if 'rap_perm_id' in dados:
            self.rap_perm_id = dados['rap_perm_id']
    
    def registrar_novo_rel_acesso_perm(self) -> dict:
        rel_existente = self.session.query(RelAcessoPermn_model).filter_by(rap_acesso_id=self.rap_acesso_id, rap_perm_id=self.rap_perm_id).first()
        if rel_existente:
            return {"msg": f"Já existe um relacionamento entre o acesso '{self.rap_acesso_id}' e o permissão '{self.rap_perm_id}'. Por favor, verifique!", "registro": False}
        
        try:
            self.session.add(self)
            self.session.commit()
            return {"msg": "Relacionamento de acesso e permissão registrado com sucesso!", "registro": True}
        except Exception as e:
            self.session.rollback()

    def ler_rel_acesso_perm_por_id(self, rap_id:int):
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