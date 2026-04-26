# ACEest Fitness & Gym DevOps Assignment

This repository contains the CI/CD and Kubernetes deployment work for the ACEest Fitness & Gym Flask application.

Repository:
`https://github.com/gourav-joshi224/gym-devops-project`

Working branch used for the assignment:
`assignment-part2`
 
## Assignment Scope

The project includes:

- Flask application source code
- Pytest-based test cases
- Jenkins pipeline as code in `Jenkinsfile`
- SonarQube scan configuration
- Docker image build and push workflow
- Kubernetes manifests for multiple deployment strategies

## Project Files

Main assignment files:

- `app.py`
- `aceest_app/`
- `tests/test_app.py`
- `Jenkinsfile`
- `Dockerfile`
- `sonar-project.properties`
- `k8s/rolling/deployment.yaml`
- `k8s/canary/deployment.yaml`
- `k8s/blue-green/deployment-blue.yaml`
- `k8s/shadow/deployment.yaml`
- `k8s/ab-testing/deployment.yaml`

## CI/CD Pipeline

The Jenkins pipeline performs these stages:

1. Checkout source from GitHub
2. Create Python virtual environment
3. Install dependencies from `requirements.txt`
4. Run Pytest and generate `pytest.xml`
5. Run SonarQube analysis
6. Enforce SonarQube quality gate
7. Build Docker image
8. Push Docker image to Docker Hub
9. Deploy rolling update to Kubernetes

Docker image used by the pipeline:

`gouravj224/aceest-fitness-gym`

## Jenkins Configuration Used

The pipeline expects the following Jenkins setup:

- SonarQube server name: `SonarQube`
- Sonar scanner tool name: `sonar-scanner`
- Docker Hub credentials id: `dockerhub-credentials`
- Kubernetes file credential id: `kubeconfig`

## SonarQube

Static analysis is configured through `sonar-project.properties`.

Project values:

- Project key: `aceest-fitness-gym`
- Project name: `ACEest Fitness & Gym`
- Python version: `3.12`

## Docker

The project is containerized using the provided `Dockerfile`.

Pipeline image tags include:

- Jenkins build number
- `latest`

## Kubernetes Deployment Strategies

The `k8s/` folder contains manifests for:

- Rolling update
- Canary deployment
- Blue-green deployment
- Shadow deployment
- A/B testing

The Jenkins pipeline currently deploys using:

- `k8s/rolling/deployment.yaml`

## Submission Notes

For assignment submission, include:

- project source folder
- GitHub repository link
- Jenkins pipeline evidence
- SonarQube quality gate/report evidence
- Docker Hub tags evidence
- Kubernetes deployment evidence
- short project report
