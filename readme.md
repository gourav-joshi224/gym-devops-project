# ACEest Fitness & Gym DevOps Pipeline

This repository contains the part 2 assignment implementation for ACEest Fitness & Gym. The project now uses a modular Flask web application backed by SQLite and is prepared for automated CI/CD delivery through Jenkins, SonarQube, Docker, and Kubernetes deployment strategies.

## Current Application Scope

The web application covers the core gym-management flow needed for the assignment:

- dashboard with client and workout overview
- client registration workflow
- client profile page
- workout logging per client
- SQLite-backed persistence through a reusable Flask app factory

## Project Structure

```text
gym-devops-project/
├── aceest_app/
│   ├── __init__.py
│   ├── db.py
│   ├── routes.py
│   ├── schema.sql
│   └── templates/
├── tests/
│   └── test_app.py
├── k8s/
│   ├── rolling/
│   ├── blue-green/
│   ├── canary/
│   ├── shadow/
│   └── ab-testing/
├── Jenkinsfile
├── Dockerfile
├── sonar-project.properties
├── requirements.txt
└── app.py
```

## Local Development

Install dependencies:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Run the Flask application:

```bash
python3 app.py
```

Open:

```text
http://127.0.0.1:5000
```

Run tests:

```bash
pytest -q
```

## Jenkins Pipeline

The committed `Jenkinsfile` converts the earlier Jenkins UI job into pipeline-as-code and adds part 2 stages:

1. Checkout source
2. Create Python virtual environment
3. Install dependencies
4. Run Pytest with JUnit output
5. Run SonarQube analysis
6. Enforce quality gate
7. Build Docker image
8. Push image to Docker Hub
9. Deploy rolling update to Kubernetes

Expected Jenkins credentials and tools:

- Sonar scanner tool named `sonar-scanner`
- SonarQube server named `SonarQube`
- Docker Hub credentials id `dockerhub-credentials`
- Kubernetes kubeconfig file credentials id `kubeconfig`

## Docker

Build locally:

```bash
docker build -t aceest-fitness-gym:local .
```

Run locally:

```bash
docker run -p 5000:5000 aceest-fitness-gym:local
```

The container uses `gunicorn` to serve the Flask application on port `5000`.

## Kubernetes Deployment Strategies

The `k8s/` directory contains example manifests for:

- Rolling Update
- Blue-Green Deployment
- Canary Release
- Shadow Deployment
- A/B Testing

Before applying manifests, replace the placeholder image:

```text
your-dockerhub-user/aceest-fitness-gym:<tag>
```

Apply the rolling deployment example:

```bash
kubectl apply -f k8s/rolling/deployment.yaml
```

## SonarQube

Static analysis is configured through `sonar-project.properties`. The Jenkins pipeline runs `sonar-scanner` and waits for the quality gate before continuing to image publishing and deployment.

## Assignment Evidence To Collect

For final submission, capture:

- GitHub repository link
- Jenkins pipeline success screenshots
- SonarQube project report screenshot
- Docker Hub repository with tagged images
- Minikube or cluster endpoint URL
- screenshots or notes showing each deployment strategy
- short architecture report describing the CI/CD flow and key challenges
