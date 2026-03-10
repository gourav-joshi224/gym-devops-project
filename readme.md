# 🏋️ Gym DevOps CI/CD Pipeline Project

---

## 📌 Project Overview

This project demonstrates the implementation of **DevOps principles** by building a CI/CD pipeline for a simple **Flask-based Gym Management Application**.

The pipeline automates the following stages of the software delivery lifecycle:

- Pulling source code from GitHub
- Installing dependencies
- Running automated tests
- Building a Docker container
- Integrating with Jenkins for Continuous Integration

---

## 🏗️ Pipeline Architecture

```
Developer
    ↓
GitHub Repository
    ↓
GitHub Actions (CI)
    ↓
Jenkins Server
    ↓
Install Dependencies
    ↓
Run Automated Tests (Pytest)
    ↓
Build Docker Image
```

---

## 📁 Project Structure

```
gym-devops-project/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
│
├── tests/
│   └── test_app.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Docker
- Jenkins (optional, for full CI pipeline)

---

## 📦 Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/gym-devops-project.git
cd gym-devops-project
```

---

## 📦 Step 2 — Dependency Management

**`requirements.txt`**
```
flask
pytest
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🧪 Step 3 — Automated Testing with Pytest

**`tests/test_app.py`**
```python
from app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
```

Run tests locally:
```bash
pytest
```

Expected output:
```
1 passed
```

---

## 🐳 Step 4 — Docker Containerization

The application is containerized using Docker to ensure consistent runtime environments across all machines.

**`Dockerfile`**
```dockerfile
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
```

Build the Docker image:
```bash
docker build -t gym-app .
```

Run the container:
```bash
docker run -p 5000:5000 gym-app
```

The app will be accessible at `http://localhost:5000`.

---

## ⚙️ Step 5 — GitHub Actions CI/CD

**`.github/workflows/ci.yml`** automates the pipeline on every push.

Pipeline tasks:
1. Checkout repository
2. Set up Python environment
3. Install dependencies
4. Run tests with Pytest
5. Build Docker image

This ensures every code push is **automatically validated** before merging.

---

## 🤖 Step 6 — Jenkins Continuous Integration

Jenkins is used to create a CI pipeline connected to the GitHub repository.

Jenkins pipeline tasks:
1. Pull latest code from GitHub
2. Install Python dependencies
3. Run automated tests
4. Build Docker image

---

## ✅ CI/CD Benefits

| Benefit | Description |
|---|---|
| Automated Testing | Tests run on every push — no manual effort needed |
| Continuous Integration | Code is validated before it reaches production |
| Faster Feedback | Developers are notified of failures immediately |
| Consistent Environments | Docker ensures the app runs the same everywhere |
| Improved Reliability | Automated pipelines reduce human error |

---

## 📄 License

This project was created for academic purposes as part of a DevOps coursework assignment.