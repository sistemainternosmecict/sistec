from waitress import serve
from flskr.app import create_app
from modules.utilidades.ferramentas import Ferramentas
import sys, os, logging, socket

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flskr'))
logging.basicConfig(level=logging.INFO)

def obter_ip():
    try:
        return socket.gethostbyname(socket.gethostname())  # Obtém o IP da máquina
    except Exception as e:
        print(f"Erro ao obter IP: {e}")
        return None

ferramentas = Ferramentas()
export_path = "./export"

if obter_ip() == "172.20.1.108":
    export_path = "/var/www/files"

app = create_app()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8082)
