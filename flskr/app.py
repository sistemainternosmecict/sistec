import sys, os, secrets
from flask import Flask, Blueprint
from flask_cors import CORS
# from flask_socketio import SocketIO

# socketio = SocketIO(app, cors_allowed_origins="http://192.168.100.131:5173")

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["*", "http://192.168.100.131", "http://192.168.100.131:5173", "http://127.20.1.108", "http://localhost"])
    app.secret_key = secrets.token_hex(32)
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.join(root_path, 'modules'))

    from .modules.usuarios import bp_usuarios, bp_niveis_acesso, bp_permissoes, bp_rap
    from .modules.demandas import bp_demandas
    from .modules.termos import bp_termos
    from .modules.dispositivos import bp_dispositivos, bp_categorias_dispositivos

    bp_api = Blueprint('api', __name__, url_prefix='/api')

    bp_api.register_blueprint(bp_usuarios)
    bp_api.register_blueprint(bp_niveis_acesso)
    bp_api.register_blueprint(bp_permissoes)
    bp_api.register_blueprint(bp_rap)
    bp_api.register_blueprint(bp_demandas)
    bp_api.register_blueprint(bp_termos)
    bp_api.register_blueprint(bp_dispositivos)
    bp_api.register_blueprint(bp_categorias_dispositivos)
    app.register_blueprint(bp_api)

    return app