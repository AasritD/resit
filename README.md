# MLaaS Resit Project

**Machine-Learning-as-a-Service (MLaaS) Prototype**  
A distributed microservices architecture paired with an Advanced AI pipeline for predicting insurance claim settlement values. Demonstrates:

- **Distributed & Enterprise Software**: containerized microservices (Auth, Billing, Training, Inference, Frontend), orchestrated with Docker Compose, plus CI/CD.  
- **Advanced AI**: DVC-managed data ingestion, hyperparameter tuning, fairness analysis, SHAP explainability, and an interactive Jupyter notebook demo.

---

## 📖 Table of Contents

1. [Project Overview](#project-overview)  
2. [High-Level Architecture](#high-level-architecture)  
3. [Directory Structure](#directory-structure)  
4. [Services & Modules](#services--modules)  
5. [Ethics & GDPR](#ethics--gdpr)  
6. [Setup](#setup)  
7. [Interactive Notebook](#interactive-notebook)  
8. [Infrastructure & Orchestration](#infrastructure--orchestration)  
9. [Continuous Integration & Delivery](#continuous-integration--delivery)  
10. [Contributing](#contributing)  
11. [License](#license)  

---

## 1. Project Overview

This repo implements:

- A **microservices** backend for user management, billing, model training & inference.  
- An **AI service** that ingests claims data, trains regressors (DecisionTree, XGBoost, RandomForest), evaluates fairness by age × gender, and produces SHAP explanations.  
- A **React frontend** (in `services/frontend/`) for interacting with the inference API.  
- A **Jupyter notebook** (`notebooks/master_notebook.ipynb`) tying together data loading, preprocessing, tuning, fairness checks, SHAP plots, and a live prediction demo.

---

## 2. High-Level Architecture

![Architecture Diagram](docs/architecture.png)  
*(See `docs/architecture.md` for a UML component diagram and rationale.)*

---

## 3. Directory Structure

```
/project-root
├── data/                       # Raw & DVC-tracked datasets  
├── docs/                       # GDPR, architecture, ethics  
├── notebooks/                  # Master Jupyter notebook demo  
├── services/
│   ├── auth/                   # Django-DRF auth service  
│   ├── billing/                # Billing microservice  
│   ├── training/               # Model training pipeline  
│   ├── inference/              # Model inference service  
│   └── frontend/               # React SPA  
├── tests/                      # pytest unit & integration tests  
├── dvc.yaml                    # DVC pipeline definition  
├── requirements.txt            # Python dependencies (frozen)  
├── Dockerfile / docker-compose.yml  
├── README.md  
└── .github/workflows/ci.yml    # CI/CD pipeline  
```

---

## 4. Services & Modules

- **AI Module** (`services/training/` & `services/inference/`)  
- **Auth Module** (`services/auth/`)  
- **Billing Module** (`services/billing/`)  
- **Training Module** (`services/training/`)  
- **Frontend** (`services/frontend/`)  

Each backend is a standalone Django + DRF app, containerized via Docker, with its own CI checks.

---

## 5. Ethics & GDPR

See [docs/gdpr.md](docs/gdpr.md) for our data-protection, anonymisation, and fairness-testing procedures, aligned with the ICO’s AI & Data Protection Toolkit.

---

## 6. Setup

Reproduce the environment and run the full pipeline:

```bash
# 1. Clone & enter repo
git clone https://github.com/AasritD/resit.git
cd resit

# 2. Create & activate a virtual environment
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# 3. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. (If using DVC)
dvc pull            # fetch data artifacts
dvc repro           # run data pipeline

# 5. Launch the notebook or services
jupyter lab         # run the AI notebook
docker-compose up   # start all microservices
```

---

## 7. Interactive Notebook

🔗 [Open `notebooks/master_notebook.ipynb`](notebooks/master_notebook.ipynb)  
Walks through data loading, preprocessing, tuning, fairness analysis, SHAP explainability, and a live prediction demo.

---

## 8. Infrastructure & Orchestration

- **Docker Compose** (`docker-compose.yml`) spins up:  
  - PostgreSQL, Redis, Nginx (reverse proxy)  
  - Auth, Billing, Training, Inference, Frontend containers  
- **Health endpoints** on each service for readiness checks.

---

## 9. Continuous Integration & Delivery

Configured via **GitHub Actions** (`.github/workflows/ci.yml`):

- Linting & type-checking (flake8, mypy)  
- pytest unit & integration tests  
- DVC pull & repro  
- Jupyter notebook execution & artifact upload  

---

## 10. Contributing

1. Fork & clone the repo.  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/awesome-improvement
   ```  
3. Make changes, commit, push, and open a Pull Request.  
4. CI will run automatically; please ensure all tests & the notebook pass.

---

## 11. License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
