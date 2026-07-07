from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import os

from app.schema import NetworkTraffic


# ==============================
# FastAPI App
# ==============================

app = FastAPI(
    title="Network Intrusion Detection API",
    description="ML based Network Intrusion Detection System using XGBoost",
    version="1.0.0"
)


# ==============================
# Load Model Artifacts
# ==============================

MODEL_PATH = "models/intrusion_model.pkl"
ENCODER_PATH = "models/label_encoder.pkl"
FEATURE_PATH = "models/feature_columns.pkl"


model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)
feature_columns = joblib.load(FEATURE_PATH)


# ==============================
# Health Check
# ==============================

@app.get("/")
def home():

    return {
        "status": "running",
        "service": "Network Intrusion Detection API",
        "model": "XGBoost"
    }


# ==============================
# Prediction API
# ==============================

@app.post("/predict")
def predict(data: NetworkTraffic):

    try:

        input_features = data.features


        # Convert input to dataframe

        df = pd.DataFrame(
            [input_features]
        )


        # Ensure correct feature order

        df = df.reindex(
            columns=feature_columns,
            fill_value=0
        )


        # Prediction

        prediction = model.predict(df)


        # Decode label

        attack_type = label_encoder.inverse_transform(
            prediction
        )[0]


        return {

            "prediction": int(prediction[0]),
            "attack_type": attack_type,
            "message": "Traffic classified successfully"

        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )