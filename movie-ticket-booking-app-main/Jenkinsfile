pipeline {
    agent any

    environment {
        VENV = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh 'python -m venv ${VENV}'
                sh './${VENV}/bin/pip install --upgrade pip'
                sh './${VENV}/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh './${VENV}/bin/python manage.py test'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("ticket_booking_system:latest")
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy stage - implement deployment steps here'
                // For example, push docker image to registry or deploy to server
            }
        }
    }
}
