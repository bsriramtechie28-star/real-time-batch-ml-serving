# Real-Time and Batch ML Serving Platform

## Overview

This project demonstrates a production-style machine learning serving platform built using Python, Scikit-Learn, FastAPI, Docker, and GitHub.

The solution predicts whether a NYC taxi trip is likely to be a high-fare trip and supports both real-time API inference and large-scale batch scoring workflows.

Key capabilities include:

* End-to-end ML training pipeline
* Feature engineering and data validation
* Real-time REST API serving with FastAPI
* Batch prediction pipeline for large datasets
* Docker containerization
* Benchmark documentation
* Git-based development workflow

---

## Business Problem

Transportation and mobility platforms often need to identify potentially high-value trips in real time for pricing analysis, resource planning, demand forecasting, and operational decision-making.

This project builds a machine learning solution capable of classifying trips as high-fare or non-high-fare based on information available before or near trip start.

---

## Dataset

Source:

NYC TLC Yellow Taxi Trip Records (January 2024)

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

These fields contain information that becomes available only after trip completion and would introduce target leakage.

---

## Project Structure

```text
app/
    main.py

src/
    train.py
    batch_predict.py
    check_data.py

docs/
    dataset.md
    design_notes.md

benchmarks/
    benchmark.md

models/
    high_fare_model.pkl

Dockerfile
requirements.txt
README.md
.gitignore
```

---

## Environment Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
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

These results were obtained using a Random Forest classifier on the January 2024 dataset.

---

## Real-Time API Serving

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

Available endpoints:

```text
GET /
POST /predict
```

### Example Request

```json
{
  "passenger_count": 2,
  "trip_distance": 10.5,
  "pickup_hour": 18
}
```

### Example Response

```json
{
  "high_fare_trip": 1
}
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

This workflow demonstrates offline scoring using the same model artifact utilized by the real-time API.

---

## Docker Deployment

Build image:

```bash
docker build -t high-fare-api .
```

Run container:

```bash
docker run -p 8000:8000 high-fare-api
```

Access API documentation:

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

This project demonstrates several production-oriented ML engineering practices:

* Feature leakage prevention
* Model serialization
* Real-time inference architecture
* Batch scoring architecture
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
* Cloud deployment (AWS, Azure, GCP)

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
