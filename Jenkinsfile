pipeline {
    agent any

    environment {
        // Définir le chemin du workspace (point de montage)
        WORKSPACE_DIR = "/workspace"
    }

    stages {
        stage('Checkout') {
            steps {
                // Pas besoin de checkout Git si on utilise le volume
                echo "Using local workspace at ${WORKSPACE_DIR}"
            }
        }

        stage('Install dependencies and test') {
            steps {
                script {
                    // Installer les dépendances backend et lancer les tests (à créer)
                    dir("${WORKSPACE_DIR}/backend") {
                        sh 'pip install -r requirements.txt'
                        sh 'python -m pytest || true'  // On ignore l'échec pour le moment car nous n'avons pas de tests
                    }
                    dir("${WORKSPACE_DIR}/frontend") {
                        sh 'pip install -r requirements.txt'
                        sh 'python -m pytest || true'
                    }
                }
            }
        }

        stage('Build Docker images') {
            steps {
                script {
                    // Construire les images Docker
                    sh "docker build -t flask-backend:latest ${WORKSPACE_DIR}/backend"
                    sh "docker build -t flask-frontend:latest ${WORKSPACE_DIR}/frontend"
                }
            }
        }

        stage('Push to registry (optional)') {
            when {
                // Par exemple, ne push que sur la branche main
                branch 'main'
            }
            steps {
                script {
                    // À configurer si on a un registre Docker
                    echo "Pushing images to registry (not implemented)"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
    }
}