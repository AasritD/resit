# MLaaS Resit Project

**A Machine-Learning-as-a-Service (MLaaS) prototype** demonstrating both AI functionality (inference & training) and distributed software-development practices (containerization, CI/CD).

---

## 📖 Table of Contents

1. [Project Overview](#project-overview)  
2. [High-Level Architecture](#high-level-architecture)  
3. [Directory Structure](#directory-structure)  
4. [Services & Modules](#services--modules)  
   - [AI Module](#ai-module)  
   - [Auth Module](#auth-module)  
   - [Billing Module](#billing-module)  
   - [Training Module](#training-module)  
   - [Frontend](#frontend)  
5. [Infrastructure & Orchestration](#infrastructure--orchestration)  
6. [Continuous Integration & Delivery](#continuous-integration--delivery)  
7. [Getting Started](#getting-started)  
8. [How to Contribute](#how-to-contribute)  
9. [License](#license)  

---

## 🚀 Project Overview

This project implements a **Machine-Learning-as-a-Service** platform with:

- **Inference Service**: Users upload data and receive model predictions.  
- **Training Service**: Engineers run offline training jobs, track experiments and publish new models.  
- **Billing Service**: Tracks usage of the inference API and generates invoices.  
- **Auth Service**: Manages users, roles (admin / engineer / finance / end-user), and GDPR-compliant endpoints.  
- **Frontend SPA**: A React-based dashboard unifying the above into a single user interface.  

All services run in isolated Docker containers, orchestrated via Docker Compose. A PostgreSQL database service holds shared data (users, logs, billing records, experiment metadata).

---

## 🏗 High-Level Architecture

```
                                   ┌────────────┐
                                   │  Frontend  │  ←─ React/Tailwind SPA
                                   └────────────┘
                                         │
┌──────────┐   ┌──────────────┐   ┌───────────────┐   ┌───────────────┐
│ Inference│   │  Training    │   │   Billing     │   │     Auth      │
│  Service │   │  Service     │   │   Service     │   │   Service     │
└──────────┘   └──────────────┘   └───────────────┘   └───────────────┘
       │              │                  │                   │
       └───────►──────┴──────────►───────┴──────────►────────┘
                         PostgreSQL Database
```

- Each microservice is a standalone Django + DRF project, with its own models, serializers, views and URLs.
- The **Docker Compose** file brings up:
  - Four service containers  
  - One `db` container for PostgreSQL  

---

## 📂 Directory Structure

```
mlaas/                         ← Repo root
├── docs/                     ← Templates & specifications
├── data/                     ← Synthetic CSV dataset
├── infrastructure/           ← Docker Compose + env files
├── .github/                  ← CI/CD workflows
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── services/                 ← All backend microservices
│   ├── inference/             
│   ├── training/              
│   ├── billing/               
│   └── users/                 
├── frontend/                 ← React Single-Page App
└── README.md                 ← This file
```

---

## 🔧 Services & Modules

### AI Module

#### 1. Inference Service  
- **Path**: `services/inference/`  
- **Purpose**:  
  - Accept user file uploads (text/image/video/audio).  
  - Run the latest model to produce a prediction.  
  - Log the input, model artifact used, and prediction in the database.  
- **Key files**:  
  - `models.py` (ModelArtifact, InferenceLog)  
  - `serializers.py` (DRF serializers)  
  - `views.py` (upload & predict endpoint)  
  - `templates/inference/upload.html` (basic upload form)  

#### 2. Training Service  
- **Path**: `services/training/`  
- **Purpose**:  
  - Ingest the synthetic insurance-claims CSV.  
  - Train Decision Trees, XGBoost or hybrid models.  
  - Track experiments via DRF and/or MLflow.  
- **Key files**:  
  - `scripts/ingest.py` & `scripts/train.py` (CLI training jobs)  
  - `models.py` (ExperimentRun, Metrics)  
  - `views.py` (trigger retrain, list past runs)  

---

### Supporting Modules

#### 3. Billing Service  
- **Path**: `services/billing/`  
- **Purpose**:  
  - Count inference calls per user.  
  - Generate invoices or billing records in PDF/JSON.  
  - Expose a finance dashboard for admins.  

#### 4. Auth Service  
- **Path**: `services/users/`  
- **Purpose**:  
  - Manage user accounts and roles (end-user / engineer / finance / admin).  
  - Issue JWT or OAuth2 tokens.  
  - Provide GDPR features (data export, right-to-be-forgotten).  

---

### Frontend

- **Path**: `frontend/`  
- **Tech**: React + Vite + Tailwind (or CRA)  
- **Purpose**:  
  - Unified UI for Inference, Training, Billing, and User management.  
  - Interactive charts (e.g. model performance, billing summary).  

---

## 🛠 Infrastructure & Orchestration

- **Docker Compose** (`infrastructure/docker-compose.yml`):  
  - Defines one container per service + `db`.  
  - Exposes ports 8001–8004 for API services, 5432 for the database.  
- **Environment file** (`infrastructure/.env`):  
  - Keeps secrets and credentials out of source control.  

---

## 🚦 Continuous Integration & Delivery

- **CI** (`.github/workflows/ci.yml`):  
  - Lints (Flake8), type-checks (mypy), runs unit/integration tests for each microservice on push and PR.  
- **CD** (`.github/workflows/cd.yml`):  
  - On merge to `main`, builds Docker images and (optionally) deploys to a staging environment.  

---

## 🏁 Getting Started

1. **Clone the repo**  
   ```bash
   git clone https://your.git.repo/mlaas.git
   cd mlaas
   ```

2. **Set up environment**  
   - Copy `.env.example` to `.env` and fill in `DB_PASSWORD`, any API keys.

3. **Launch services**  
   ```bash
   cd infrastructure
   docker-compose up --build
   ```

4. **Browse the APIs**  
   - Inference:  `http://localhost:8001/api/artifacts/`  
   - Training:   `http://localhost:8002/api/experiments/`  
   - Billing:    `http://localhost:8003/api/invoices/`  
   - Auth:       `http://localhost:8004/api/users/`  

5. **Run tests**  
   ```bash
   docker-compose exec inference python app/manage.py test
   docker-compose exec training python app/manage.py test
   # etc.
   ```

---

## 🤝 How to Contribute

1. Pick an issue or module you want to work on.  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/awesome-improvement
   ```
3. Commit your changes, push, and open a Pull Request.  
4. CI will run automatically; code reviews are appreciated.  

---

## Ethics & GDPR  
See [docs/gdpr.md](docs/gdpr.md) for details on data protection, anonymisation, and fairness checks.  
