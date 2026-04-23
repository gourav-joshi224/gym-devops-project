pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        VENV_DIR = ".venv"
    }

    stages {
        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Set Up Python Environment") {
            steps {
                sh """
                    echo "Starting Jenkins build..."
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage("Run Pytest") {
            steps {
                sh """
                    . ${VENV_DIR}/bin/activate
                    pytest -q --junitxml=pytest.xml
                """
            }
        }

        stage("Build Docker Image") {
            steps {
                sh 'docker build -t gym-app:${BUILD_NUMBER} -t gym-app:latest .'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'tests/**/*.py', allowEmptyArchive: true
            junit allowEmptyResults: true, testResults: 'pytest.xml'
        }
        cleanup {
            sh 'rm -rf ${VENV_DIR}'
        }
    }
}
