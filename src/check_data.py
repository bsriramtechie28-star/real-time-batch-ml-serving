import pandas as pd

df = pd.read_parquet("data/yellow_tripdata_2024-01.parquet")

print("Shape:", df.shape)

print("\nColumns:")
for col in df.columns:
    print(col)

print("\nFare amount distribution:")
print(df["fare_amount"].describe())