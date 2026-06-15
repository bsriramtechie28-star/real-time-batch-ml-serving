# Benchmark results
## Environment 
- Local windows Machine 
- python 3.14
- FastAPI
- Random Forest classifer 

## Model performance 
Accuracy: 94%

class 0:
- precision: 0.95
- recall 0.97

Class 1:
- precision: 0.92
- recall: 0.85

# real-time API 

Endpoint:
POST/predict 

Containerized using Docker.

## Batch Scoring 

Dataset:
January 2024 NYC TLC Trips

Records Processed:
2,964,624

output:
data/batch_predictions.csv

## observations
- single modle artifact  used for both real-time and batch interference
- FastAPI provides low-latency online predections.
- Batch pipeline supports large-scale offline scoring.
- Docker container enables deployment portability.