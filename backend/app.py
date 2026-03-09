from flask import Flask, jsonify, request
import logging
from pythonjsonlogger import jsonlogger
from prometheus_flask_exporter import PrometheusMetrics
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle pour les items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Création des tables et ajout de quelques données initiales
with app.app_context():
    db.create_all()
    # Ajouter des données exemple si la table est vide
    if Item.query.count() == 0:
        sample_items = [
            Item(name="Laptop", description="Ordinateur portable 16 Go RAM"),
            Item(name="Souris", description="Souris sans fil"),
            Item(name="Clavier", description="Clavier mécanique")
        ]
        db.session.bulk_save_objects(sample_items)
        db.session.commit()

# Exporter Prometheus
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

# Configuration du logger JSON
log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
log_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

@app.route('/health')
def health():
    logger.info("Health check called")
    return jsonify({"status": "ok"})

@app.route('/api/data')
def get_data():
    logger.info("Data endpoint called")
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

# (Optionnel) Endpoint pour ajouter un nouvel item
@app.route('/api/data', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    new_item = Item(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(new_item)
    db.session.commit()
    logger.info(f"New item added: {new_item.name}")
    return jsonify(new_item.to_dict()), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5030)