pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        VENV_DIR = ".venv"
        SONAR_SCANNER_HOME = tool 'sonar-scanner'
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

        stage("Run SonarQube Analysis") {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        . ${VENV_DIR}/bin/activate
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner
                    """
                }
            }
        }

        stage("Enforce Quality Gate") {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
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
