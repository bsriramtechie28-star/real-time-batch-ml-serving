from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(
    title="High Fare Trip Prediction API"
)

model = joblib.load("models/high_fare_model.pkl")


class TripRequest(BaseModel):
    passenger_count: int
    trip_distance: float
    pickup_hour: int


@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/predict")
def predict(request: TripRequest):

    data = pd.DataFrame(
        [{
            "passenger_count": request.passenger_count,
            "trip_distance": request.trip_distance,
            "pickup_hour": request.pickup_hour
        }]
    )

    prediction = model.predict(data)[0]

    return {
        "high_fare_trip": int(prediction)
    }