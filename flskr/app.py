import sys, os
from flask import Flask, jsonify

app = Flask(__name__)

app.secret_key = "test"

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(root_path, 'modules'))

from ..modules.usuarios import Gerenciador_usuarios

@app.route('/', methods=['GET'])
def index():
    GU = Gerenciador_usuarios()
    usuario = GU.carregar_solicitante_via_id(2)
    # res = usuario['dados']
    # if 'dados' in usuario:
    return jsonify({'nome':usuario})