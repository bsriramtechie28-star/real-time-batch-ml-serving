# Prediction Task

## Objective

Predict whether a taxi trip is likely to be a high-fare trip using information available at trip start time.

---

## Target Definition

```text
high_fare_trip = 1 if fare_amount >= 20.5
high_fare_trip = 0 otherwise
```

The threshold was selected using the 75th percentile of the January 2024 NYC TLC Yellow Taxi dataset.

Fare statistics:

* Median fare: $12.80
* 75th percentile fare: $20.50

Trips with fare amounts greater than or equal to $20.50 represent approximately the highest-value 25% of trips, making this a practical classification problem for both real-time and batch inference.

---

## Why This Target

* Practical business use case for demand planning and driver allocation.
* Suitable for both real-time and batch inference.
* Supports low-latency online predictions.
* Easy to explain, benchmark, and operationalize.
* Avoids reliance on post-trip calculations during serving.

---

## Features Used

The baseline model uses only information that is reasonably available before or at trip initiation:

* passenger_count
* trip_distance
* pickup_hour

Derived Features:

* pickup_hour (extracted from tpep_pickup_datetime)

Additional features such as VendorID, PULocationID, DOLocationID, and pickup_dayofweek were evaluated but excluded from the baseline implementation to keep the model simple and aligned with project time constraints.

---

## Data Leakage Prevention

The following fields were intentionally excluded from model training because they become available only after or during trip completion and would introduce target leakage:

* fare_amount
* total_amount
* tip_amount
* tolls_amount
* congestion_surcharge
* Airport_fee
* improvement_surcharge
* tpep_dropoff_datetime

The target label is derived from fare_amount, but fare_amount itself is never used as a model feature.

The model was restricted to information realistically available before prediction time to ensure consistent behavior in both online and batch inference scenarios.

---

## Architecture Overview

```text
NYC TLC Dataset
        |
        v
     train.py
        |
        v
high_fare_model.pkl
        |
   +----+----+
   |         |
   v         v
FastAPI   batch_predict.py
 Online    Batch Scoring
   |            |
   v            v
Prediction   CSV Output
```

Both online and batch inference reuse the same trained model artifact (`high_fare_model.pkl`) to ensure prediction consistency across serving paths.

---

## Serving Design

### Real-Time Inference

* FastAPI REST endpoint
* Pydantic request validation
* Single-record prediction support
* Swagger/OpenAPI documentation
* Preloaded model for low-latency inference

### Batch Inference

* Offline scoring using input datasets
* Generates prediction output files
* Reuses the same trained model artifact as the online service

### Model Artifact

* Serialized using Joblib
* Shared between online and batch inference paths
* Versioned through Git-based releases

---

## Assumptions

* Passenger count is known before trip completion.
* Trip distance estimates are available at prediction time.
* Pickup hour is available when prediction is requested.
* January 2024 TLC data is representative of normal trip behavior.
* High-fare trips are defined as fare_amount >= 20.5.

---

## Deployment Considerations

### Resource Requirements

Recommended deployment resources:

* CPU Request: 0.5 vCPU
* CPU Limit: 2 vCPU
* Memory Request: 512 MB
* Memory Limit: 1 GB

### Readiness Behavior

The application is considered ready when:

* FastAPI starts successfully.
* The trained model artifact is loaded into memory.

### Liveness Behavior

The root endpoint (`GET /`) can be used as a basic health check.

Expected response:

```json
{
  "status": "running"
}
```

### Autoscaling Considerations

For production deployment, scaling can be driven by:

* CPU utilization
* Request volume
* Response latency

Because inference is stateless and the model is loaded during startup, multiple container replicas can serve requests concurrently behind a load balancer.

---

## Baseline Model

Model:

* RandomForestClassifier

Features:

* passenger_count
* trip_distance
* pickup_hour

Results:

* Accuracy: 94%
* Precision (high_fare_trip): 92%
* Recall (high_fare_trip): 85%
* F1-score (high_fare_trip): 88%

Reasoning:

A Random Forest was selected as a strong baseline for tabular data with minimal feature engineering while maintaining good predictive performance and deployment simplicity.

---

## Model Selection Trade-offs

### Logistic Regression

Pros:

* Fast training and inference
* Highly interpretable
* Small memory footprint

Cons:

* Limited ability to model nonlinear relationships
* May underperform on complex tabular datasets

Decision:

Considered as a baseline but not selected because taxi trip behavior contains nonlinear patterns that tree-based models capture more effectively.

---

### Random Forest (Selected)

Pros:

* Captures nonlinear feature interactions
* Robust against overfitting
* Minimal feature preprocessing required
* Strong performance on tabular datasets

Cons:

* Larger model size
* Less interpretable than linear models

Decision:

Selected because it achieved strong predictive performance while remaining simple to train, deploy, and maintain.

---

### XGBoost

Pros:

* State-of-the-art performance on many tabular datasets
* Strong handling of complex feature interactions
* Built-in regularization

Cons:

* Requires additional hyperparameter tuning
* Increased implementation complexity
* Longer experimentation cycle

Decision:

Not selected for the initial implementation due to project time constraints. It remains a strong candidate for future optimization.

---

## Future Improvements

* Model monitoring and drift detection
* MLflow experiment tracking
* Automated CI/CD pipeline
* Container orchestration with Kubernetes
* Load testing and latency benchmarking
* Feature store integration
* Hyperparameter optimization
* Automated retraining workflows
* Centralized logging and observability
