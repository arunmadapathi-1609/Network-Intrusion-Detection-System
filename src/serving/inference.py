import pandas as pd

from src.serving.model_loader import load_model

# Load model and artifacts once
model, label_encoder, feature_columns = load_model()

def predict(features):

    # Convert input to DataFrame
    if isinstance(features, dict):
        input_df = pd.DataFrame([features])
    else:
        input_df = pd.DataFrame(features)

    # Remove unwanted spaces from column names
    input_df.columns = input_df.columns.str.strip()

    # Match training feature order
    input_df = input_df.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # Prediction
    predictions = model.predict(input_df)

    probabilities = model.predict_proba(input_df)

    attack_types = label_encoder.inverse_transform(
        predictions
    )

    results = []

    for pred, attack, prob in zip(predictions, attack_types, probabilities):

        traffic_status = (
            "🟢 Safe Traffic"
            if attack.upper() == "BENIGN"
            else "🔴 Malicious Traffic"
        )

        results.append(
            {
                "prediction_id": int(pred),
                "attack_type": str(attack),
                "confidence": round(
                    float(prob.max()),
                    4
                ),
                "traffic_status": traffic_status
            }
        )


    return results