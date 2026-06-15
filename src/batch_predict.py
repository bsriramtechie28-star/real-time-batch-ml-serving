import pandas as pd
import joblib

print("Loading model...")

model = joblib.load("models/high_fare_model.pkl")

print("Loading dataset...")

df = pd.read_parquet("data/yellow_tripdata_2024-01.parquet")

# same feature engineering used during training
df = df[df["fare_amount"] > 0]

df["pickup_hour"] = pd.to_datetime(
    df["tpep_pickup_datetime"]
).dt.hour

X = df[
    [
        "passenger_count",
        "trip_distance",
        "pickup_hour"
    ]
].fillna(0)

print("Generating predictions...")

df["predicted_high_fare_trip"] = model.predict(X)

output_file = "data/batch_predictions.csv"

df[
    [
        "passenger_count",
        "trip_distance",
        "pickup_hour",
        "predicted_high_fare_trip"
    ]
].to_csv(output_file, index=False)

print(f"Predictions saved to {output_file}")