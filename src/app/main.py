from typing import List

from fastapi import FastAPI, HTTPException, Body

from src.app.schemas import NetworkFlow
from src.serving.inference import predict

app = FastAPI(
    title="Network Intrusion Detection API",
    description="End-to-End Network Intrusion Detection System using XGBoost",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "status": "running",
        "project": "Network Intrusion Detection System",
        "algorithm": "XGBoost"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# Single Prediction
@app.post("/predict")
def predict_endpoint(data: NetworkFlow):
    try:
        result = predict(data.model_dump(by_alias=True))
        return result[0]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Batch Prediction
@app.post("/predict_batch")
def predict_batch_endpoint(
    data: List[dict] = Body(...)
):
    try:
        return predict(data)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )