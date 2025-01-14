from waitress import serve
from flskr.app import create_app
import sys, os, logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flskr'))
logging.basicConfig(level=logging.INFO)

app = create_app()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8082, threads=4)
