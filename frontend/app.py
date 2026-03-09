from flask import Flask, render_template
import requests
import logging
from pythonjsonlogger import jsonlogger
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Frontend app info', version='1.0.0')

# Configuration du logger JSON
log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
log_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

BACKEND_URL = "http://backend:5030"

@app.route('/')
def index():
    logger.info("Index page accessed")
    try:
        response = requests.get(f"{BACKEND_URL}/api/data")
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        data = []
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5031)