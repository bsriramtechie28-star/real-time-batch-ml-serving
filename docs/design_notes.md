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

- Passenger count is known before trip completion.
- Trip distance estimate is available at prediction time.
- Pickup hour is available when prediction is requested.
- January 2024 TLC data is representative of normal trip behavior.
- High-fare trips are defined as fare_amount >= 20.5.

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
## Model Selection Trade-offs

### Logistic Regression

Pros:
- Fast training and inference
- Highly interpretable
- Small memory footprint

Cons:
- Limited ability to model nonlinear relationships
- May underperform on complex tabular datasets

Decision:
- Considered as a baseline but not selected because trip behavior exhibits nonlinear patterns that tree-based models capture more effectively.

### Random Forest (Selected)

Pros:
- Captures nonlinear feature interactions
- Robust against overfitting
- Minimal feature preprocessing required
- Strong performance on tabular datasets

Cons:
- Larger model size
- Less interpretable than linear models

Decision:
- Selected because it achieved strong predictive performance while remaining simple to train, deploy, and maintain.

### XGBoost

Pros:
- State-of-the-art performance on many tabular datasets
- Strong handling of complex interactions
- Built-in regularization

Cons:
- Requires additional hyperparameter tuning
- Increased implementation complexity

Decision:
- Not selected for the initial implementation due to project time constraints. Considered a strong candidate for future optimization.

### Data Leakage Prevention

To ensure realistic predictions, the following fields were excluded from training:

- fare_amount
- total_amount
- tip_amount
- tolls_amount

These attributes become available after or during trip completion and would introduce target leakage. The model was restricted to information realistically available before prediction time.