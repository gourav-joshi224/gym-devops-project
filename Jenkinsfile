pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        VENV_DIR = ".venv"
        SONAR_SCANNER_HOME = tool 'sonar-scanner'
        IMAGE_NAME = "your-dockerhub-user/aceest-fitness-gym"
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
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage("Push Docker Image") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh """
                        echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${IMAGE_NAME}:latest
                        docker logout
                    """
                }
            }
        }

        stage("Deploy Rolling Update to Kubernetes") {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        kubectl apply -f k8s/rolling/deployment.yaml
                        kubectl set image deployment/aceest-fitness aceest-fitness=${IMAGE_NAME}:${BUILD_NUMBER}
                        kubectl rollout status deployment/aceest-fitness --timeout=120s
                    """
                }
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
