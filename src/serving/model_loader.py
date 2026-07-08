from pathlib import Path

import joblib

# =====================================================
# Model Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "intrusion_model.pkl"
ENCODER_PATH = BASE_DIR / "models" / "label_encoder.pkl"
FEATURE_PATH = BASE_DIR / "models" / "feature_columns.pkl"


# =====================================================
# Load Model Artifacts
# =====================================================

def load_model():

    """
    Load all model artifacts.

    Returns
    -------
    tuple
        (model, label_encoder, feature_columns)
    """

    model = joblib.load(MODEL_PATH)

    label_encoder = joblib.load(ENCODER_PATH)

    feature_columns = joblib.load(FEATURE_PATH)

    return model, label_encoder, feature_columns