FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose le port 5030 (port utilisé par le backend)
EXPOSE 5030

# Commande pour lancer l'application
CMD ["python", "app.py"]