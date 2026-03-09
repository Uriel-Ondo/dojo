# Dojo DevOps – Plateforme de démonstration

Bienvenue dans le projet **Dojo DevOps** !  
Cette plateforme a pour but de mettre en pratique les concepts DevOps à travers une application Flask complète, conteneurisée, monitorée et outillée avec des outils open‑source.

L'objectif est de disposer d'un environnement de développement local reproductible, permettant d'expérimenter avec :

- Une application **Flask** à deux services (backend API + frontend avec templates)
- **Docker** et **Docker Compose** pour l'orchestration locale
- **Prometheus** + **Grafana** pour le monitoring
- **Loki** + **Promtail** pour la centralisation des logs
- **cAdvisor** pour les métriques des conteneurs
- **Jenkins** (optionnel) pour l'intégration continue
- Un frontend enrichi avec des icônes et des liens vers tous les services

---

## 🧱 Architecture

```
[ Utilisateur ] ↔ [ Frontend (Flask, port 5031) ] ↔ [ Backend API (Flask, port 5030) ]
                          │                                    │
                          ▼                                    ▼
                    [ Grafana (3020) ]                  [ Prometheus (9090) ]
                          │                                    │
                          ▼                                    ▼
                    [ Loki (3100) ]                      [ cAdvisor (8084) ]
                          │
                          ▼
                    [ Promtail ]
```

Tous les services sont interconnectés via un réseau Docker dédié (`app-network`).

---

## 📋 Prérequis

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 ou supérieure)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29 ou supérieure)
- Git (pour cloner le dépôt)

---

## 🚀 Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/Uriel-Ondo/dojo.git
   cd dojo
   ```

2. **Lancer tous les services**
   ```bash
   docker compose up -d
   ```

3. **Vérifier que tous les conteneurs sont bien démarrés**
   ```bash
   docker compose ps
   ```

   Vous devriez voir les conteneurs suivants (selon votre configuration) :
   - `flask-backend`
   - `flask-frontend`
   - `prometheus`
   - `grafana`
   - `loki`
   - `promtail`
   - `cadvisor`
   - `jenkins` (optionnel)

---

## 🔗 Accès aux services

| Service       | URL                                      | Identifiants par défaut |
|---------------|------------------------------------------|--------------------------|
| Frontend      | http://localhost:5031                    | -                        |
| Backend API   | http://localhost:5030/health              | -                        |
| Prometheus    | http://localhost:9090                     | -                        |
| Grafana       | http://localhost:3020                     | `admin` / `admin`        |
| Loki (via Grafana) | http://localhost:3020/explore (sélectionner Loki) | – |
| cAdvisor      | http://localhost:8084                     | -                        |
| Jenkins       | http://localhost:8080                     | (à configurer au premier démarrage) |

> 💡 Tous les liens sont également disponibles depuis le tableau de bord du frontend (page d'accueil).

---

## 📦 Services détaillés

### Backend (Flask)
- **Rôle** : API REST fournissant des données (ex: `/api/data`).
- **Port** : `5030`
- **Métriques Prometheus** : exposées sur `/metrics`
- **Logs** : format JSON, collectés par Promtail.

### Frontend (Flask)
- **Rôle** : interface utilisateur avec `render_template`. Affiche les données de l'API et un tableau de bord des services.
- **Port** : `5031`
- **Métriques Prometheus** : exposées sur `/metrics`
- **Logs** : format JSON, collectés par Promtail.

### Prometheus
- **Rôle** : collecte des métriques depuis le backend, le frontend, et éventuellement cAdvisor.
- **Port** : `9090`
- **Configuration** : montée via `./prometheus.yml`

### Grafana
- **Rôle** : visualisation des métriques (Prometheus) et des logs (Loki).
- **Port** : `3020`
- **Sources de données pré-configurées** : Prometheus et Loki.
- **Dashboards** : à importer ou créer selon les besoins.

### Loki
- **Rôle** : agrégateur de logs léger.
- **Port** : `3100` (interne, non exposé directement)
- **Configuration** : `loki-config.yml`

### Promtail
- **Rôle** : agent de collecte des logs. Il lit les logs des conteneurs Docker via le socket Docker et les envoie à Loki.
- **Configuration** : `promtail-config.yml`

### cAdvisor
- **Rôle** : expose les métriques d'utilisation des ressources des conteneurs (CPU, mémoire, réseau, etc.).
- **Port** : `8084`
- **Intégration** : Prometheus peut scraper cAdvisor pour enrichir le monitoring.

### Jenkins (optionnel)
- **Rôle** : serveur d'intégration continue.
- **Port** : `8080`
- **Note** : à déployer séparément ou via un `docker-compose` dédié (voir dossier `jenkins/`).

---

## 📊 Utilisation courante

### Générer du trafic / des logs
- Accédez au frontend (http://localhost:5031) et rafraîchissez plusieurs fois.
- Appelez directement l'API : `curl http://localhost:5030/api/data`

### Visualiser les logs dans Grafana
1. Ouvrez Grafana (http://localhost:3020).
2. Allez dans **Explore**.
3. Choisissez la source **Loki**.
4. Utilisez l'explorateur de labels ou entrez une requête comme `{container="flask-frontend"}`.

### Consulter les métriques
- Dans Prometheus : http://localhost:9090 (exemple de requête : `flask_http_request_total`)
- Dans Grafana : créez un dashboard ou importez-en un existant (par exemple [3662](https://grafana.com/grafana/dashboards/3662) pour Flask).

### Arrêter / relancer la plateforme
```bash
# Arrêter tous les services
docker compose down

# Relancer en arrière-plan
docker compose up -d

# Voir les logs en temps réel
docker compose logs -f
```

### Reconstruire une image après modification du code
```bash
docker compose build backend    # ou frontend, etc.
docker compose up -d backend
```

---

## ⚙️ Configuration avancée

### Variables d'environnement
- **Backend** : `FLASK_ENV` (development/production)
- **Frontend** : `BACKEND_URL` (URL du backend, par défaut `http://backend:5030`)

### Personnalisation des ports
Vous pouvez modifier les ports exposés dans le fichier `docker-compose.yml`. Attention aux éventuels conflits.

### Ajout d'un nouveau service
1. Créez son Dockerfile et sa configuration.
2. Ajoutez-le au `docker-compose.yml`.
3. Mettez à jour le frontend (`index.html`) pour ajouter un lien vers ce service.

---

## 🐛 Dépannage

### Problème : impossible d'accéder à Grafana
- Vérifiez le mapping de ports : `3020:3000` dans `docker-compose.yml`.
- Consultez les logs : `docker-compose logs grafana`

### Problème : Loki ne démarre pas (erreur de permission)
- Assurez-vous que le répertoire `./loki-data` existe et a les droits d'écriture :  
  ```bash
  mkdir -p loki-data && chmod 777 loki-data
  ```

### Problème : Promtail ne collecte pas les logs
- Vérifiez que le socket Docker est monté (`/var/run/docker.sock`).
- Regardez les logs de Promtail : `docker-compose logs promtail`

### Problème : les conteneurs ne se parlent pas entre eux
- Tous les services doivent être sur le même réseau (`app-network`). Vérifiez dans `docker-compose.yml`.

---

## 🤝 Contribution

Les contributions sont les bienvenues !  
- Signalez un bug via une *issue*.
- Proposez une amélioration via une *pull request*.
- Pour les modifications du code Flask, pensez à mettre à jour les tests et la documentation.

---

## 📄 Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le distribuer.

---

**Amusez-vous bien avec cette plateforme DevOps !**  
Si vous avez des questions, n'hésitez pas à ouvrir une issue.