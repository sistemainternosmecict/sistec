from waitress import serve
from flskr.app import create_app, app
from modules.utilidades.ferramentas import Ferramentas
import sys, os, logging, schedule, time, threading, socket

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flskr'))
logging.basicConfig(level=logging.INFO)

def obter_ip():
    try:
        return socket.gethostbyname(socket.gethostname())  # Obtém o IP da máquina
    except Exception as e:
        print(f"Erro ao obter IP: {e}")
        return None

def rodar_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

ferramentas = Ferramentas()
export_path = "./export"

if obter_ip() == "172.20.1.108":
    export_path = "/var/www/files"

socketio = create_app()

schedule.every(1).hour.do(ferramentas.limpar_pdfs, export_path)
threading.Thread(target=rodar_scheduler, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8082, debug=True)
