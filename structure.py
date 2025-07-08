import os

# Project layout definition
structure = {
    "docs": [
        "SprintReviewTemplate.docx",
        "TaskDeliveryForm.docx",
        "ResitSpecs.pdf",
        "MarkingRubric.pdf",
        "CaseStudyMLaaS.pdf"
    ],
    "data": [
        "Synthetic_Data_For_Students.csv"
    ],
    "infrastructure": [
        "docker-compose.yml",
        ".env"
    ],
    ".github/workflows": [
        "ci.yml",
        "cd.yml"
    ],
    "services/inference": [
        "Dockerfile",
        "requirements.txt"
    ],
    "services/inference/app": [
        "manage.py"
    ],
    "services/inference/app/inference_project": [
        "__init__.py",
        "settings.py",
        "urls.py",
        "wsgi.py"
    ],
    "services/inference/app/inference_app": [
        "__init__.py",
        "models.py",
        "serializers.py",
        "views.py",
        "urls.py",
        "forms.py",
        "tests.py"
    ],
    "services/inference/app/inference_app/templates/inference": [
        "upload.html"
    ],
    "services/training": [
        "Dockerfile",
        "requirements.txt"
    ],
    "services/training/app": [
        "manage.py"
    ],
    "services/training/app/training_project": [
        "__init__.py",
        "settings.py",
        "urls.py",
        "wsgi.py"
    ],
    "services/training/app/training_app": [
        "__init__.py",
        "models.py",
        "serializers.py",
        "views.py",
        "urls.py",
        "tests.py"
    ],
    "services/training/app/training_app/scripts": [
        "ingest.py",
        "train.py"
    ],
    "services/billing": [
        "Dockerfile",
        "requirements.txt"
    ],
    "services/billing/app": [
        "manage.py"
    ],
    "services/billing/app/billing_project": [
        "__init__.py",
        "settings.py",
        "urls.py",
        "wsgi.py"
    ],
    "services/billing/app/billing_app": [
        "__init__.py",
        "models.py",
        "serializers.py",
        "views.py",
        "urls.py",
        "tests.py"
    ],
    "services/billing/app/billing_app/templates/billing": [
        "dashboard.html"
    ],
    "services/users": [
        "Dockerfile",
        "requirements.txt"
    ],
    "services/users/app": [
        "manage.py"
    ],
    "services/users/app/users_project": [
        "__init__.py",
        "settings.py",
        "urls.py",
        "wsgi.py"
    ],
    "services/users/app/users_app": [
        "__init__.py",
        "models.py",
        "serializers.py",
        "views.py",
        "urls.py",
        "tests.py"
    ],
    "services/users/app/users_app/templates/users": [
        "profile.html"
    ],
    "frontend": [
        "Dockerfile",
        "package.json"
    ],
    "frontend/public": [],
    "frontend/src": [
        "App.jsx"
    ],
    "": [
        "README.md",
        "LICENSE"
    ]
}

# File contents for those that need boilerplate
boilerplate = {
    "infrastructure/docker-compose.yml": """\
version: '3.8'
services:
  inference:
    build: ./services/inference
    depends_on:
      - db
    ports:
      - "8001:8000"
  training:
    build: ./services/training
    depends_on:
      - db
    ports:
      - "8002:8000"
  billing:
    build: ./services/billing
    depends_on:
      - db
    ports:
      - "8003:8000"
  users:
    build: ./services/users
    depends_on:
      - db
    ports:
      - "8004:8000"
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mlaas_db
      POSTGRES_USER: mlaas_user
      POSTGRES_PASSWORD: secretpassword
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:
""",
    ".github/workflows/ci.yml": """\
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [inference, training, billing, users]
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install deps
        run: |
          cd services/${{ matrix.service }}
          pip install --upgrade pip
          pip install -r requirements.txt
      - name: Lint & type-check
        run: |
          pip install flake8 mypy
          flake8 --max-line-length=120
          mypy app
      - name: Run tests
        run: |
          python app/manage.py test
""",
    ".github/workflows/cd.yml": """\
name: CD
on:
  push:
    branches:
      - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Deploy to staging
        run: echo "Add your deployment scripts here"
""",
    "README.md": """\
# MLaaS Resit Project

## Overview
- **AI Module**: Inference & Training services
- **Auth**: User service (roles & GDPR)
- **Billing**: Usage billing service
- **Frontend**: React SPA
- **Distributed Dev**: Docker Compose orchestration & CI/CD

## Running Locally
```bash
cd infrastructure
docker-compose up --build
```"""
}

def create_project(structure_map, boilerplate_map, base_dir="."):
    for rel_dir, files in structure_map.items():
        target_dir = os.path.join(base_dir, rel_dir) if rel_dir else base_dir
        os.makedirs(target_dir, exist_ok=True)

        for fname in files:
            full_path = os.path.join(target_dir, fname)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            content = boilerplate_map.get(os.path.join(rel_dir, fname), "")
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created {full_path}")

if __name__ == "__main__":
    create_project(structure, boilerplate)
