# Real-Time and Batch ML Serving

## Overview

This project implements a machine learning solution using the NYC TLC January 2024 trip dataset.

The objective is to predict whether a taxi trip is likely to be a high-fare trip.

The solution supports:

- Model training
- Real-time inference via FastAPI
- Batch inference for large datasets
- Docker containerization
- Benchmark documentation

---

## Dataset

NYC TLC Yellow Taxi January 2024 dataset

Dataset file:

data/yellow_tripdata_2024-01.parquet

---

## Prediction Target

high_fare_trip = 1 if fare_amount >= 20.5

high_fare_trip = 0 otherwise

---

## Model Training

Generate the model artifact:

```bash
python src/train.py
```

This creates:

```text
models/high_fare_model.pkl
```

---

## Run Real-Time API

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

---

## Batch Prediction

```bash
python src/batch_predict.py
```

Output:

```text
data/batch_predictions.csv
```

---

## Docker

Build image:

```bash
docker build -t high-fare-api .
```

Run container:

```bash
docker run -p 8000:8000 high-fare-api
```

Open:

```text
http://localhost:8000/docs
```

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
```

---

## Performance

Model Accuracy: 94%

See:

benchmarks/benchmark.md