# 🛡️ Network Intrusion Detection System

```{=html}
<p align="center">
```
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.47-FF4B4B?logo=streamlit)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker)

```{=html}
</p>
```
## 📌 Project Overview

An end-to-end Machine Learning project that detects malicious network
traffic using **XGBoost**. The application provides a **FastAPI REST
API** for inference and a **Streamlit dashboard** for batch CSV
prediction. It follows a modular, production-oriented structure and is
containerized with Docker for reproducible deployment.

## 🎯 Problem Statement

Modern networks generate massive traffic, making manual inspection
impractical. This project automatically classifies network flows as
**BENIGN** or **Malicious**, helping accelerate security analysis.

### Key Features

-   XGBoost-based intrusion detection
-   FastAPI REST API
-   Streamlit batch prediction UI
-   CSV upload & download
-   Confidence score for each prediction
-   Docker support
-   Modular project structure

## 🏗️ Architecture

``` text
Network Traffic CSV
        │
        ▼
 Data Preprocessing
        │
        ▼
 Feature Alignment
        │
        ▼
   XGBoost Model
        │
  ┌─────┴─────┐
  ▼           ▼
FastAPI   Streamlit
  │           │
  └─────┬─────┘
        ▼
 Prediction Results
```

## 📂 Project Structure

``` text
Network-Intrusion-Detection-System/
├── Data/
├── models/
├── notebooks/
├── scripts/
├── src/
│   ├── app/
│   ├── serving/
│   ├── features/
│   ├── data/
│   └── utils/
├── streamlit_app/
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## 🛠️ Tech Stack

  Category     Technologies
  ------------ -----------------------
  ML           XGBoost, Scikit-learn
  Backend      FastAPI, Uvicorn
  Frontend     Streamlit
  Data         Pandas, NumPy
  Deployment   Docker, Render

## 🚀 Local Setup

``` bash
git clone https://github.com/arunmadapathi-1609/Network-Intrusion-Detection-System.git
cd Network-Intrusion-Detection-System

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### Run FastAPI

``` bash
python -m uvicorn src.app.main:app --reload
```

Swagger: http://127.0.0.1:8000/docs

### Run Streamlit

``` bash
streamlit run streamlit_app/app.py
```

Dashboard: http://localhost:8501

## 📡 API

  Method   Endpoint         Description
  -------- ---------------- -------------------
  GET      /                API status
  GET      /health          Health check
  POST     /predict         Single prediction
  POST     /predict_batch   Batch prediction

### Example Response

``` json
{
  "prediction_id": 0,
  "attack_type": "BENIGN",
  "confidence": 0.9987,
  "traffic_status": "🟢 Safe Traffic"
}
```

## 🐳 Docker

``` bash
docker build -t network-intrusion-detection .
docker run -p 8000:8000 -p 8501:8501 network-intrusion-detection
```

## ☁️ Deployment

Deploy the Docker image to Render or another container platform.

## 🔮 Future Improvements

-   Real-time packet capture
-   SHAP explainability
-   Authentication
-   MLflow model registry
-   GitHub Actions CI/CD
