import os

import pandas as pd
import requests

# FastAPI Endpoint

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000/predict_batch"
)
# Batch Prediction

def predict_batch(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Send network traffic data to the FastAPI backend
    and return predictions as a DataFrame.
    """

    payload = input_df.to_dict(
        orient="records"
    )

    response = requests.post(
        API_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    predictions = pd.DataFrame(
        response.json()
    )

    return predictions