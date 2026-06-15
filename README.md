# Real-Time and Batch ML Serving Platform

## Overview

This project demonstrates an end-to-end machine learning serving platform built using Python, Scikit-Learn, FastAPI, Docker, and GitHub.

The solution predicts whether a NYC taxi trip is likely to be a high-fare trip and supports both real-time API inference and large-scale batch scoring workflows.

Key capabilities include:

* Data exploration and target definition
* Feature engineering and leakage prevention
* Model training using Random Forest
* Real-time inference using FastAPI
* Batch prediction pipeline
* Docker containerization
* Benchmark documentation
* Production-style project structure

---

## Quick Start

### Clone Repository

```bash
git clone https://github.com/bsriramtechie28-star/real-time-batch-ml-serving.git
cd real-time-batch-ml-serving
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Train Model

```bash
python src/train.py
```

This creates:

```text
models/high_fare_model.pkl
```

### Start API

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

### Test Prediction Endpoint

Example Request:

```json
{
  "passenger_count": 2,
  "trip_distance": 10.5,
  "pickup_hour": 18
}
```

Example Response:

```json
{
  "high_fare_trip": 1
}
```

### Run Batch Predictions

```bash
python src/batch_predict.py
```

Output:

```text
data/batch_predictions.csv
```

### Run Using Docker

Build Image:

```bash
docker build -t high-fare-api .
```

Run Container:

```bash
docker run -p 8000:8000 high-fare-api
```

Open:

```text
http://localhost:8000/docs
```

---

## Business Problem

Transportation and mobility platforms often need to identify potentially high-value trips for pricing analysis, operational planning, demand forecasting, and resource allocation.

This project builds a machine learning solution capable of classifying trips as high-fare or non-high-fare using information available before or near trip start.

---

## Dataset

Dataset:

NYC TLC Yellow Taxi Trip Records – January 2024

Expected location:

```text
data/yellow_tripdata_2024-01.parquet
```

The dataset is intentionally excluded from source control because of its size.

---

## Prediction Objective

Target Variable:

```text
high_fare_trip
```

Definition:

```text
1 = High Fare Trip
0 = Non High Fare Trip
```

The target is derived using the 75th percentile of fare values from the dataset.

---

## Solution Architecture

```text
Raw Dataset
      │
      ▼
Feature Engineering
      │
      ▼
Model Training
      │
      ▼
Random Forest Model
      │
 ┌────┴────┐
 ▼         ▼
Batch      Real-Time
Scoring    API Serving
```

---

## Features Used

The model uses only information available before or near trip start:

* passenger_count
* trip_distance
* pickup_hour

### Leakage Prevention

The following fields are intentionally excluded:

* fare_amount
* total_amount
* tip_amount
* tolls_amount
* dropoff timestamps

These fields contain information available only after trip completion and would introduce target leakage.

---

## Project Structure

```text
app/
│   main.py
│
benchmarks/
│   benchmark.md
│
docs/
│   dataset.md
│   design_notes.md
│
models/
│   high_fare_model.pkl
│
src/
│   train.py
│   batch_predict.py
│   check_data.py
│
Dockerfile
requirements.txt
README.md
.gitignore
.dockerignore
```

---

## Model Training

Train the model:

```bash
python src/train.py
```

Generated artifact:

```text
models/high_fare_model.pkl
```

---

## Model Performance

| Metric    | Score |
| --------- | ----- |
| Accuracy  | 94%   |
| Precision | 0.92  |
| Recall    | 0.85  |
| F1 Score  | 0.88  |

Detailed benchmark information is available in:

```text
benchmarks/benchmark.md
```

---

## Real-Time API

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

Available Endpoints:

```text
GET /
POST /predict
```

---

## Batch Prediction Pipeline

Generate predictions for large datasets:

```bash
python src/batch_predict.py
```

Output:

```text
data/batch_predictions.csv
```

The same trained model is used for both batch and real-time inference.

---

## Docker Deployment

Build:

```bash
docker build -t high-fare-api .
```

Run:

```bash
docker run -p 8000:8000 high-fare-api
```

Access:

```text
http://localhost:8000/docs
```

---

## Documentation

Additional project documentation:

```text
docs/dataset.md
docs/design_notes.md
benchmarks/benchmark.md
```

---

## Engineering Considerations

This project demonstrates several production-oriented machine learning engineering practices:

* Feature leakage prevention
* Model serialization
* Batch inference workflows
* Real-time API serving
* Docker containerization
* Reproducible development workflow
* Documentation-driven development

---

## Future Enhancements

Potential improvements include:

* Automated unit testing
* GitHub Actions CI/CD pipeline
* MLflow experiment tracking
* Model versioning
* Automated benchmark reporting
* Monitoring and drift detection
* Cloud deployment on AWS, Azure, or GCP

---

## Technologies Used

* Python
* Pandas
* Scikit-Learn
* FastAPI
* Uvicorn
* Docker
* Git
* GitHub

---

## Author

**Sriram B**

Senior AI/ML Engineer

Production-style machine learning serving platform demonstrating model training, batch inference, real-time API serving, and containerized deployment.
