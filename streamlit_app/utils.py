import pandas as pd

# Merge Original Data with Predictions

def merge_predictions(original_df: pd.DataFrame, predictions: pd.DataFrame) -> pd.DataFrame:

    return pd.concat(
        [
            original_df.reset_index(drop=True),
            predictions.reset_index(drop=True)
        ],
        axis=1
    )

# Calculate Risk Level

def calculate_risk_level(malicious_percent: float) -> str:

    if malicious_percent <= 5:
        return "🟢 Low"

    elif malicious_percent <= 15:
        return "🟡 Medium"

    elif malicious_percent <= 30:
        return "🟠 High"

    else:
        return "🔴 Critical"

# Generate Security Summary

def calculate_summary(
    result: pd.DataFrame
) -> dict:
    """
    Calculate dashboard statistics.
    """

    safe_count = (result["traffic_status"].str.contains("Safe").sum())

    malicious_count = (result["traffic_status"].str.contains("Malicious").sum())

    total = len(result)

    safe_percent = round(safe_count / total * 100, 2)

    malicious_percent = round(malicious_count / total * 100, 2)

    risk_level = calculate_risk_level(malicious_percent)

    return {
        "total": total,
        "safe_count": safe_count,
        "malicious_count": malicious_count,
        "safe_percent": safe_percent,
        "malicious_percent": malicious_percent,
        "risk_level": risk_level,
    }