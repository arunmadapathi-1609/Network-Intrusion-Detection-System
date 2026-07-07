import os
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ==============================
# Paths
# ==============================

DATA_PATH = "data/processed/network_intrusion_small.csv"

MODEL_PATH = "models/intrusion_model.pkl"
ENCODER_PATH = "models/label_encoder.pkl"
FEATURE_PATH = "models/feature_columns.pkl"


# ==============================
# Load Dataset
# ==============================

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Dataset Shape:", df.shape)


# ==============================
# Load Model Artifacts
# ==============================

print("\nLoading trained model...")

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)
feature_columns = joblib.load(FEATURE_PATH)

print("Model loaded successfully")


# ==============================
# Prepare Data
# ==============================

TARGET_COLUMN = "Label"

X = df[feature_columns]
y = df[TARGET_COLUMN]


# ==============================
# Encode Labels
# ==============================

y_encoded = label_encoder.transform(y)


# ==============================
# Prediction
# ==============================

print("\nRunning predictions...")

y_pred = model.predict(X)


# ==============================
# Evaluation Metrics
# ==============================

accuracy = accuracy_score(
    y_encoded,
    y_pred
)

precision = precision_score(
    y_encoded,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_encoded,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_encoded,
    y_pred,
    average="weighted",
    zero_division=0
)


# ==============================
# Print Results
# ==============================

print("\n" + "=" * 60)
print("NETWORK INTRUSION DETECTION MODEL EVALUATION")
print("=" * 60)

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("=" * 60)


# ==============================
# Classification Report
# ==============================

print("\nClassification Report\n")

report = classification_report(
    y_encoded,
    y_pred,
    target_names=label_encoder.classes_,
    zero_division=0
)

print(report)


# ==============================
# Confusion Matrix
# ==============================

print("\nConfusion Matrix\n")

cm = confusion_matrix(
    y_encoded,
    y_pred
)

print(cm)


# ==============================
# Save Evaluation Report
# ==============================

os.makedirs("reports", exist_ok=True)

report_path = "reports/evaluation_report.txt"

with open(report_path, "w") as f:

    f.write("NETWORK INTRUSION DETECTION MODEL EVALUATION\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Dataset Size : {df.shape}\n\n")

    f.write(f"Accuracy  : {accuracy:.4f}\n")
    f.write(f"Precision : {precision:.4f}\n")
    f.write(f"Recall    : {recall:.4f}\n")
    f.write(f"F1 Score  : {f1:.4f}\n\n")

    f.write("Classification Report\n")
    f.write("-" * 40 + "\n")
    f.write(report)

    f.write("\nConfusion Matrix\n")
    f.write("-" * 40 + "\n")
    f.write(str(cm))


print("\nEvaluation report saved successfully!")
print(f"Location: {report_path}")

print("\nEvaluation Completed Successfully!")