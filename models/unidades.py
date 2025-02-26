from sqlalchemy import Column, Integer, String, Boolean, create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import logging, os
from dotenv import load_dotenv

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

class Unidade_model(Base):
    __tablename__ = 'tb_unidades'

    uni_id = Column(Integer, primary_key=True, autoincrement=True)
    uni_registro = Column(String(14))
    uni_cod_ue = Column(Integer, nullable=False)
    uni_designador_categoria = Column(String(25), nullable=True)
    uni_nome = Column(String(100), nullable=False)
    uni_cep = Column(Integer, nullable=False)
    uni_logradouro = Column(String(50))
    uni_numero_end = Column(Integer)
    uni_bairro = Column(String(50))
    uni_distrito = Column(String(2))
    uni_direcao = Column(String(50))
    uni_telefone_direcao = Column(String(12))
    uni_segmentos = Column(String(100))
    uni_listada = Column(Boolean, default=False)

    def __init__(self):
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url, echo=True, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def __repr__(self):
        return f"<Unidade(uni_id={self.uni_id}, uni_nome='{self.uni_nome}', uni_cod_ue={self.uni_cod_ue})>"

    def criar_unidade(self):
        unidade_existente = self.session.query(self.__class__).filter_by(uni_nome=self.uni_nome).first()
        
        if unidade_existente:
            return {"msg": "Unidade com este nome já existe!", "registro": False}
        
        # unidade_existente = self.session.query(self.__class__).filter_by(uni_cod_ue=self.uni_cod_ue).first()
        
        # if unidade_existente:
        #     return {"msg": "Unidade com este código UE já existe!", "registro": False}
        
        todos_os_registros = self.ler_todos("uni_cod_ue")

        codigos = [reg.uni_cod_ue for reg in todos_os_registros]

        if self.uni_cod_ue in codigos:
            index = codigos.index(self.uni_cod_ue)

            primeira_lista = todos_os_registros[:index]
            segunda_lista = todos_os_registros[index:]

            nova_unidade = Unidade_model()
            nova_unidade.uni_cod_ue = self.uni_cod_ue
            nova_unidade.uni_registro = self.uni_registro
            nova_unidade.uni_designador_categoria = self.uni_designador_categoria
            nova_unidade.uni_nome = self.uni_nome
            nova_unidade.uni_cep = self.uni_cep
            nova_unidade.uni_logradouro = self.uni_logradouro
            nova_unidade.uni_numero_end = self.uni_numero_end
            nova_unidade.uni_bairro = self.uni_bairro
            nova_unidade.uni_distrito = self.uni_distrito
            nova_unidade.uni_direcao = self.uni_direcao
            nova_unidade.uni_telefone_direcao = self.uni_telefone_direcao
            nova_unidade.uni_segmentos = self.uni_segmentos
            nova_unidade.uni_listada = self.uni_listada

            for unidade in segunda_lista:
                unidade.uni_cod_ue += 1
        
            self.session.add(nova_unidade)
            self.session.commit()
            return {"msg": "Registro realizado!", "registro": True, "id_registrado": nova_unidade.uni_id}
        else:
            self.session.add(self)
            self.session.commit()
            return {"msg": "Registro realizado!", "registro": True, "id_registrado": self.uni_id}


    def buscar_por_id(self, id:int):
        unidade = self.session.query(Unidade_model).filter(Unidade_model.uni_id == id).first()
        if unidade:
            return {'unidade':unidade, 'encontrado':True}
        return {'unidade':None, 'encontrado':False}

    def buscar_por_cod_ue(self, uni_cod_ue:int):
        unidade = self.session.query(Unidade_model).filter(Unidade_model.uni_cod_ue == uni_cod_ue).first()
        if unidade:
            return {'unidade':unidade, 'encontrado':True}
        return {'unidade':None, 'encontrado':False}

    def buscar_por_categoria(self, designador_categoria:str):
        unidades =  self.session.query(Unidade_model).filter(Unidade_model.uni_designador_categoria == designador_categoria).all()
        if unidades:
            return {'unidades':unidades, 'encontrado':True}
        return {'unidades':None, 'encontrado':False}

    def ler_todos(self, ordem='uni_id'):
        if ordem == 'uni_cod_ue':
            return self.session.query(Unidade_model).order_by(Unidade_model.uni_cod_ue).all()
        elif ordem == 'uni_nome':
            return self.session.query(Unidade_model).order_by(Unidade_model.uni_nome).all()
        return self.session.query(Unidade_model).order_by(Unidade_model.uni_id).all()

    def atualizar_unidade(self, updates:dict):
        unidade = self.buscar_por_id(updates['uni_id'])
        if unidade:
            for key, value in updates.items():
                setattr(unidade['unidade'], key, value)
            self.session.commit()
            return {'atualizado':True}
        return {'atualizado':False}

    def remover_unidade(self, unidade) -> dict:
        res = { "msg":"Registro não pode ser removido!", "removido":False }
        if unidade:
            self.session.delete(unidade)
            self.session.commit()
            res = { "msg":"Registro removido!", "removido":True }
        return res

    def ativar_unidade(self, uni_id:int):
        unidade = self.buscar_por_id(uni_id)
        if unidade:
            unidade['unidade'].uni_listada = True
            self.session.commit()
            return {"ativada":True, "msg":"Unidade ativada com sucesso!"}
        return {"ativada":False, "msg":"A unidade não pôde ser ativada."}

    def desativar_unidade(self, uni_id:int):
        unidade = self.buscar_por_id(uni_id)
        if unidade:
            unidade['unidade'].uni_listada = False
            self.session.commit()
            return {"ativada":False, "msg":"Unidade desativada com sucesso!"}
        return {"ativada":True, "msg":"A unidade não pôde ser desativada."}
