from sqlalchemy import create_engine, Column, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from modules.utilidades.ferramentas import Ferramentas
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

class Usuario_model(Base):
    __tablename__ = 'tb_usuarios'

    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_matricula = Column(String(15), nullable=False)
    usuario_setor = Column(String(80), nullable=False)
    usuario_cargo = Column(String(50), nullable=False)
    usuario_nome = Column(String(128), nullable=False)
    usuario_funcao = Column(String(50), nullable=False)
    usuario_sala = Column(String(4), nullable=False)
    usuario_cpf = Column(BigInteger, nullable=False)
    usuario_email = Column(String(100), unique=True, nullable=False)
    usuario_telefone = Column(BigInteger)
    usuario_senha = Column(String(100), nullable=False)
    usuario_tipo = Column(Integer, nullable=False)
    usuario_ativo = Column(Boolean)

    def __init__(self, dados:dict=None):
        # db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        # self.engine = create_engine(db_url, echo=True)
        self.engine = create_engine('sqlite:///usuarios.db', echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
        if dados:
            self.distribuir_dados(dados)

    def __repr__(self):
        return f"""<Usuario(usuario_id={self.usuario_id}, 
        usuario_cpf={self.usuario_cpf}, 
        usuario_nome={self.usuario_nome}, 
        usuario_matricula={self.usuario_matricula}, 
        usuario_setor={self.usuario_setor}, 
        usuario_sala={self.usuario_sala}, 
        usuario_cargo={self.usuario_cargo}, 
        usuario_funcao={self.usuario_funcao}, 
        usuario_email={self.usuario_email}, 
        usuario_telefone={self.usuario_telefone}, 
        usuario_tipo={self.usuario_tipo}, 
        usuario_ativo={self.usuario_ativo})>"""
    
    def distribuir_dados(self, dados:dict) -> None:
        if 'usuario_cpf' in dados:
            self.usuario_cpf = dados['usuario_cpf']
        if 'usuario_nome' in dados:
            self.usuario_nome = dados['usuario_nome']
        if 'usuario_matricula' in dados:
            self.usuario_matricula = dados['usuario_matricula']
        if 'usuario_setor' in dados:
            self.usuario_setor = dados['usuario_setor']
        if 'usuario_sala' in dados:
            self.usuario_sala = dados['usuario_sala']
        if 'usuario_cargo' in dados:
            self.usuario_cargo = dados['usuario_cargo']
        if 'usuario_funcao' in dados:
            self.usuario_funcao = dados['usuario_funcao']
        if 'usuario_email' in dados:
            self.usuario_email = dados['usuario_email']
        if 'usuario_telefone' in dados:
            self.usuario_telefone = dados['usuario_telefone']
        if 'usuario_senha' in dados:
            self.usuario_senha = dados['usuario_senha']
        if 'usuario_tipo' in dados:
            self.usuario_tipo = dados['usuario_tipo']
        if 'usuario_ativo' in dados:
            self.usuario_ativo = dados['usuario_ativo']
    
    def obter_hash(self) -> str: #ferramenta interna do modelo que utiliza ferramenta externa
        FERRAMENTAS = Ferramentas()
        self.usuario_senha = FERRAMENTAS.encriptar_senha(self.usuario_senha)
        return self.usuario_senha

    def registrar_novo_usuario(self) -> dict:
        self.obter_hash()
        usuario_existente_matricula = self.session.query(Usuario_model).filter_by(usuario_matricula=self.usuario_matricula).first()
        if usuario_existente_matricula:
            return { "msg": f"A matrícula '{self.usuario_matricula}' já está cadastrada. Por favor, use outra matrícula!", "registro": False }
        
        usuario_existente_nome = self.session.query(Usuario_model).filter_by(usuario_nome=self.usuario_nome).first()
        if usuario_existente_nome:
            return { "msg": f"O nome '{self.usuario_nome}' já está cadastrado. Por favor, use outro nome!", "registro": False }
        
        usuario_existente_email = self.session.query(Usuario_model).filter_by(usuario_email=self.usuario_email).first()
        if usuario_existente_email:
            return { "msg": f"O email '{self.usuario_email}' já está cadastrado. Por favor, use outro email!", "registro": False }

        try:
            self.session.add(self)
            self.session.commit()
            return { "msg": "Registro realizado!", "registro": True, "id": self.usuario_id }
        except Exception as e:
            self.session.rollback()
        
    def ler_todos_os_registros(self) -> dict:
        return {'todos_usuarios':self.session.query(Usuario_model).all()}
    
    def ler_pelo_id(self, id:int) -> object:
        usuario = self.session.query(Usuario_model).filter_by(usuario_id=id).first()
        return {'usuario':usuario}
    
    def ler_pelo_cpf(self, cpf:int) -> object:
        usuario = self.session.query(Usuario_model).filter_by(usuario_cpf=cpf).first()
        return {'usuario':usuario}
    
    def ler_pelo_matricula(self, matricula:int) -> object:
        usuario = self.session.query(Usuario_model).filter_by(usuario_matricula=matricula).first()
        return {'usuario':usuario}
    
    def ler_pelo_nome(self, nome:str) -> dict:
        nome_temp = nome.lower()
        usuario_temp = self.session.query(Usuario_model).filter_by(usuario_nome=nome).first()
        if nome_temp == usuario_temp.usuario_nome.lower():
            return {'usuario':usuario_temp}
        return {'usuario':None}
    
    def atualizar_usuario(self, **kwargs) -> dict:
        modificado = []
        id = kwargs.get('usuario_id')
        usuario = self.ler_pelo_id(id)
        if usuario['usuario'] and len(kwargs) > 1:
            for key, value in kwargs.items():
                if key != 'usuario_id':
                    if key == 'usuario_senha':
                        self.usuario_senha = value
                        self.obter_hash()
                        setattr(usuario['usuario'], key, self.usuario_senha)
                        modificado.append(key)
                    else:
                        setattr(usuario['usuario'], key, value)
                        modificado.append(key)
            self.session.commit()
            return {'atualizado':True, 'modificado':modificado}
        return {'atualizado':False}

    def remover_usuario(self, usuario_id) -> dict:
        usuario = self.session.query(Usuario_model).filter(Usuario_model.usuario_id == usuario_id).first()
        if usuario:
            try:
                self.session.delete(usuario)
                self.session.commit()
                return {'removido':True}
            except Exception as e:
                print(e)
                return {'removido':False}
            
    def verificar_credenciais(self, matricula:int, senha:str) -> dict:
        usuario_temp = self.session.query(Usuario_model).filter_by(usuario_matricula=matricula).first()

        if not usuario_temp:
            return {'msg': 'Matrícula não encontrada em nosso banco de dados!', 'verificado': False}
    
    # Verifica se a senha corresponde ao hash armazenado
        if self.verificar_senha(usuario_temp, senha):
            return {'usuario':usuario_temp, 'verificado':True if usuario_temp != None else False, 'msg':'Usuário logado!'}
        return {'msg': 'Senha incorreta!', 'verificado': False}
    
    def verificar_senha(self, usuario, senha: str):
        """Verifica se a senha corresponde ao hash armazenado no banco de dados."""
        ferramentas = Ferramentas()
        senha_temp = ferramentas.encriptar_senha(senha)
        if usuario.usuario_senha == senha_temp:
            return True
        return False