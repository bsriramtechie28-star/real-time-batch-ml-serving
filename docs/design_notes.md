# Prediction Task

## Objective

Predict whether a taxi trip is likely to be a high-fare trip using information available at trip start time.

## Target Definition

high_fare_trip = 1 if fare_amount >= 20.5
high_fare_trip = 0 otherwise

Threshold selected from the 75th percentile ($20.50) of fare_amount
in the January 2024 NYC TLC dataset..

Fare statistics:

- Median fare: $12.80
- 75th percentile fare: $20.50

Trips with fare_amount >= $20.50 represent approximately the highest-value 25% of trips, making this a practical classification problem for both real-time and batch inference.

## Why This Target

- Practical business use case for demand planning and driver allocation.
- Suitable for both real-time and batch inference.
- Supports low-latency online predictions.
- Easy to explain, benchmark, and operationalize.
- Avoids reliance on post-trip calculations during serving.

## Features Used

The model will use only information available before or during trip initiation:

- VendorID
- passenger_count
- trip_distance
- PULocationID
- DOLocationID
- pickup_hour
- pickup_dayofweek

Derived Features:
- pickup_hour (from tpep_pickup_datetime)
- pickup_dayofweek (from tpep_pickup_datetime)

## Excluded Fields (Leakage)

The following fields are excluded because they are only known after trip completion and would introduce target leakage:

- total_amount
- tip_amount
- tolls_amount
- congestion_surcharge
- Airport_fee
- improvement_surcharge
- tpep_dropoff_datetime

fare_amount is used only to generate the target label and is never used as a model feature.

## Serving Design

### Real-Time Inference

- FastAPI REST endpoint
- Single-record and small-batch prediction support
- Pydantic schema validation
- Preloaded model for low-latency predictions

### Batch Inference

- Offline scoring from CSV or Parquet input files
- Generates prediction output files
- Reuses the same trained model artifact as the online service

### Model Artifact

- Serialized using Joblib
- Shared between online and batch inference paths
- Versioned through Git-based releases

## Assumptions

- January 2024 NYC TLC Yellow Taxi data is representative for local development.
- Input records conform to the published TLC schema.
- Missing values are limited and can be handled during preprocessing.
- Single-node execution is sufficient for assignment-scale workloads.

## Future Improvements

- Model monitoring and drift detection
- MLflow experiment tracking
- Automated CI/CD pipeline
- Container orchestration with Kubernetes
- Load testing and latency benchmarking
- Feature store integration 

## Baseline Model

Model:
- RandomForestClassifier

Features:
- passenger_count
- trip_distance
- pickup_hour

Results:
- Accuracy: 94%
- Precision (high_fare_trip): 92%
- Recall (high_fare_trip): 85%
- F1-score (high_fare_trip): 88%

Reasoning:
A Random Forest was selected as a strong baseline for tabular data with minimal feature engineering.