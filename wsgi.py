from waitress import serve
from flskr.app import create_app
from modules.utilidades.ferramentas import Ferramentas
import sys, os, logging, schedule, time, threading

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flskr'))
logging.basicConfig(level=logging.INFO)

ferramentas = Ferramentas()
export_path = "./export"
schedule.every(1).hour.do(ferramentas.limpar_pdfs, export_path)

def rodar_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

app = create_app()

threading.Thread(target=rodar_scheduler, daemon=True).start()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8082, threads=4)
