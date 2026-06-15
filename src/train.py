import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df = pd.read_parquet("data/yellow_tripdata_2024-01.parquet")

# remove invalid fares
df = df[df["fare_amount"] > 0]

# create target
df["high_fare_trip"] = (df["fare_amount"] >= 20.5).astype(int)

# derive feature
df["pickup_hour"] = pd.to_datetime(
    df["tpep_pickup_datetime"]
).dt.hour

# model features
X = df[
    [
        "passenger_count",
        "trip_distance",
        "pickup_hour"
    ]
].fillna(0)

y = df["high_fare_trip"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

print(classification_report(y_test, preds))