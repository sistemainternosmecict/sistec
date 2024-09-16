import sys, os, secrets
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://sistec", "http://192.168.100.131", "http://192.168.100.131:5173", "http://192.168.100.116"])
    app.secret_key = secrets.token_hex(32)
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.join(root_path, 'modules'))

    from .modules.usuarios import bp_usuarios
    from .modules.demandas import bp_demandas

    bp_api = Blueprint('api', __name__, url_prefix='/api')

    bp_api.register_blueprint(bp_usuarios)
    bp_api.register_blueprint(bp_demandas)
    app.register_blueprint(bp_api)

    return app