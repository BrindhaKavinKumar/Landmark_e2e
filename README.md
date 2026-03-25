# 🚀 Retail Data Platform – End-to-End DevOps Project

## 📌 Overview

This project is a production-style **event-driven data pipeline** that processes retail product updates from CSV files uploaded to AWS S3.

The system validates, processes, and stores data while providing full observability using Prometheus and Grafana. Infrastructure is provisioned using Terraform and CI/CD is implemented using GitHub Actions.

---

## 🏗️ Architecture

```
S3 (File Upload)
   ↓
SQS (Event Notification)
   ↓
Worker Service (Python)
   ↓
PostgreSQL (Storage)
   ↓
Prometheus (Metrics)
   ↓
Grafana (Visualization)
```

---

## ⚙️ Tech Stack

* **Cloud**: AWS (S3, SQS)
* **Backend**: Python (SQLAlchemy, Pandas)
* **Database**: PostgreSQL
* **Containerization**: Docker
* **Orchestration**: Kubernetes (Minikube)
* **Infrastructure as Code**: Terraform
* **Monitoring**: Prometheus + Grafana
* **CI/CD**: GitHub Actions

---

## 🔄 Data Flow

1. CSV file uploaded to S3 bucket
2. S3 triggers event → sent to SQS queue
3. Worker polls SQS and processes message
4. File downloaded and validated
5. Valid records → stored in DB
6. Invalid records → logged (error_logs)
7. Metrics updated and exposed via `/metrics`
8. Prometheus scrapes metrics
9. Grafana visualizes pipeline performance

---

## ✅ Features

* ✔️ Event-driven architecture (S3 → SQS)
* ✔️ Data validation rules (price, stock, etc.)
* ✔️ Partial success handling
* ✔️ Error logging with raw data
* ✔️ Idempotency (skip already processed files)
* ✔️ Metrics (files processed, failed, skipped)
* ✔️ Observability with Grafana dashboards
* ✔️ Containerized services (Docker)
* ✔️ Kubernetes deployment
* ✔️ Infrastructure provisioning using Terraform
* ✔️ CI/CD pipeline with GitHub Actions

---

## 📊 Metrics Exposed

* `files_processed_total`
* `files_failed_total`
* `files_skipped_total`
* `records_processed_total`
* `records_failed_total`
* `processing_duration_seconds`

---

## 🚀 Getting Started

### 1. Clone repo

```bash
git clone https://github.com/BrindhaKavinKumar/Landmark_e2e.git
cd Landmark_e2e
```

### 2. Run with Docker

```bash
docker compose up --build
```

### 3. Run worker locally

```bash
cd worker-service
python -m app.main
```

---

## ☁️ AWS Setup (Terraform)

```bash
cd infra
terraform init
terraform apply
```

Resources created:

* S3 bucket
* SQS queue + DLQ

---

## 📈 Monitoring

* Prometheus: http://localhost:9090
* Grafana: http://localhost:3000

Example dashboards:

* Total files processed
* Failed records
* Processing duration

---

## 🔁 CI/CD

GitHub Actions pipeline:

* Install dependencies
* Validate imports
* Run basic checks
* Build Docker image

Workflow file:

```
.github/workflows/ci.yml
```

---

## 🧠 Key Learnings

* Designing event-driven systems
* Handling failures and retries (DLQ)
* Observability and monitoring
* Infrastructure automation using Terraform
* CI/CD pipeline implementation
* Debugging real-world distributed systems

---

## 📌 Future Improvements

* Add API service for querying processed data
* Implement retry backoff strategy
* Add authentication & secrets management
* Deploy to cloud Kubernetes (EKS)
* Add alerting (Prometheus Alertmanager)

---

## 👤 Author

**Brindha**
DevOps Engineer 

---

## ⭐️ Project Highlights

This project demonstrates:

* End-to-end system design
* Production-like architecture
* DevOps best practices
* Real-world debugging & monitoring

---

🔥 *This is a complete hands-on DevOps project covering CI/CD, Kubernetes, Terraform, AWS, and Observability.*
