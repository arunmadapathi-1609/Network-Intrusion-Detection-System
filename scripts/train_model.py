from pathlib import Path
import time
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from src.features.build_features import build_features

# ---------------- Paths ---------------- #

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "Data/processed/network_intrusion_small.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

# ---------------- Load Data ---------------- #

df = pd.read_csv(DATA_PATH)

X, y, label_encoder, feature_columns = build_features(df)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------- MLflow ---------------- #

mlflow.set_tracking_uri((BASE_DIR / "mlruns").resolve().as_uri())
mlflow.set_experiment("Network Intrusion Detection")

with mlflow.start_run():

    model = XGBClassifier(
        objective="multi:softprob",
        num_class=len(label_encoder.classes_),
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        tree_method="hist",
        eval_metric="mlogloss",
        random_state=42,
        n_jobs=-1
    )

    start = time.time()

    model.fit(X_train, y_train)

    training_time = time.time() - start

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    # ---------- MLflow ---------- #

    mlflow.log_params(model.get_params())

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("training_time_sec", training_time)

    mlflow.sklearn.log_model(
        model,
        name="network_intrusion_model"
    )

# ---------------- Save Artifacts ---------------- #

joblib.dump(model, MODEL_DIR / "intrusion_model.pkl")
joblib.dump(label_encoder, MODEL_DIR / "label_encoder.pkl")
joblib.dump(feature_columns, MODEL_DIR / "feature_columns.pkl")

print("=" * 60)
print("Training Completed Successfully")
print("=" * 60)
print(f"Accuracy      : {accuracy:.4f}")
print(f"Training Time : {training_time:.2f} sec")
print("Model Saved Successfully")