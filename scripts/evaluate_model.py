from pathlib import Path
import time
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from src.features.build_features import build_features


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "Data" / "processed" / "network_intrusion_small.csv"

MODEL_DIR = BASE_DIR / "models"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

X, y, label_encoder, feature_columns = build_features(df)

# Same split used during training
_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Loading model...")

model = joblib.load(MODEL_DIR / "intrusion_model.pkl")

print("Model loaded successfully.")

start = time.time()

y_pred = model.predict(X_test)

prediction_time = time.time() - start

metrics = {
    "Accuracy": accuracy_score(y_test, y_pred),
    "Precision": precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0,
    ),
    "Recall": recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0,
    ),
    "Weighted F1": f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0,
    ),
    "Macro F1": f1_score(
        y_test,
        y_pred,
        average="macro",
        zero_division=0,
    ),
}

report = classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_,
    zero_division=0,
)

cm = confusion_matrix(y_test, y_pred)

print("\n" + "=" * 60)
print("NETWORK INTRUSION DETECTION EVALUATION")
print("=" * 60)

for name, value in metrics.items():
    print(f"{name:<15}: {value:.4f}")

print(f"Prediction Time : {prediction_time:.4f} sec")

print("=" * 60)

print("\nClassification Report\n")
print(report)

print("\nConfusion Matrix\n")
print(cm)


pd.DataFrame(
    cm,
    index=label_encoder.classes_,
    columns=label_encoder.classes_,
).to_csv(REPORT_DIR / "confusion_matrix.csv")

with open(REPORT_DIR / "evaluation_report.txt", "w") as f:

    f.write("NETWORK INTRUSION DETECTION EVALUATION\n")
    f.write("=" * 60 + "\n\n")

    for name, value in metrics.items():
        f.write(f"{name:<15}: {value:.4f}\n")

    f.write(f"\nPrediction Time : {prediction_time:.4f} sec\n\n")

    f.write("Classification Report\n")
    f.write("=" * 60 + "\n")
    f.write(report)

print("\nEvaluation completed successfully.")
print(f"Reports saved to: {REPORT_DIR}")