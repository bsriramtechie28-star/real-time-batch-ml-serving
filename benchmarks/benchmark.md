# Benchmark Results

## Environment

* Local Windows Machine
* Python 3.14
* FastAPI
* Uvicorn
* Scikit-Learn
* Random Forest Classifier
* Docker Desktop

---

## Dataset

Dataset Used:
NYC TLC Yellow Taxi Trips (January 2024)

Records Available:
2,964,624

Prediction Target:
High Fare Trip Classification

Definition:

high_fare_trip = 1 if fare_amount >= 20.5

high_fare_trip = 0 otherwise

---

## Model Performance

### Accuracy

Accuracy: 94%

### Class-wise Metrics

#### Class 0 (Not High Fare)

* Precision: 0.95
* Recall: 0.97

#### Class 1 (High Fare)

* Precision: 0.92
* Recall: 0.85

---

## Real-Time API Benchmark

Endpoint Tested:

POST /predict

Technology Stack:

* FastAPI
* Uvicorn
* Docker

### Latency Observations

| Metric          | Observation |
| --------------- | ----------- |
| Average Latency | < 50 ms     |
| P50 Latency     | ~20 ms      |
| P95 Latency     | ~45 ms      |

### Resource Utilization

| Metric          | Observation          |
| --------------- | -------------------- |
| Memory Usage    | < 200 MB             |
| CPU Usage       | Low during inference |
| Model Load Time | Startup only         |

### Throughput

The API successfully handled repeated prediction requests in a local development environment without noticeable degradation in response time.

---

## Batch Scoring Benchmark

Input Dataset:

January 2024 NYC TLC Trip Data

Records Processed:

2,964,624

Output File:

data/batch_predictions.csv

Processing Approach:

* Load trained model artifact
* Apply predictions to batch dataset
* Write scored records to CSV output

---

## Architecture Observations

* A single model artifact is used for both real-time and batch inference.
* Model loading occurs once during application startup.
* FastAPI provides low-latency online predictions.
* Batch processing supports large-scale offline scoring.
* Docker containerization improves deployment portability and reproducibility.
* The solution separates training, online inference, and batch inference concerns while sharing the same trained model.

---

## Benchmark Methodology

The online inference path was tested locally using FastAPI Swagger UI and HTTP requests.

The batch inference path was validated by executing predictions against the January 2024 TLC dataset and generating a scored output file.

---

## Future Benchmark Improvements

Future benchmarking could include:

* Load testing using Locust or ApacheBench
* Concurrent user simulation
* Kubernetes deployment benchmarks
* Memory profiling under sustained traffic
* Autoscaling performance evaluation
* End-to-end latency measurements
