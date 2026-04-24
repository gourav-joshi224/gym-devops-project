pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        VENV_DIR = ".venv"
        SONAR_SCANNER_HOME = tool 'sonar-scanner'
        IMAGE_NAME = "gouravj224/aceest-fitness-gym"
        K8S_DEPLOYMENT = "aceest-fitness"
        K8S_SELECTOR = "app=aceest-fitness"
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
                    set -eu
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
                    set -eu
                    . ${VENV_DIR}/bin/activate
                    python -m pytest -q --junitxml=pytest.xml
                """
            }
        }

        stage("Run SonarQube Analysis") {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        set -eu
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
                    sh '''
                        set -eu
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }

        stage("Deploy Rolling Update to Kubernetes") {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        set -eu
                        kubectl get nodes
                        kubectl apply -f k8s/rolling/deployment.yaml
                        kubectl set image deployment/${K8S_DEPLOYMENT} aceest-fitness=${IMAGE_NAME}:${BUILD_NUMBER}
                        kubectl rollout status deployment/${K8S_DEPLOYMENT} --timeout=300s || {
                            kubectl describe deployment/${K8S_DEPLOYMENT}
                            kubectl describe pods -l ${K8S_SELECTOR}
                            exit 1
                        }
                        kubectl get pods -l ${K8S_SELECTOR} -o wide
                        kubectl get svc aceest-fitness-service
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
