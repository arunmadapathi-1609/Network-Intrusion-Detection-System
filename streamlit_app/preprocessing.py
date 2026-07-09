import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:

    input_df = df.copy()

    # Remove unwanted spaces from column names
    input_df.columns = input_df.columns.str.strip()

    # Remove target columns if present
    target_columns = [
        "Label",
        "label",
        "Attack",
        "attack"
    ]

    input_df = input_df.drop(
        columns=[
            col for col in target_columns
            if col in input_df.columns
        ],
        errors="ignore"
    )

    # Replace infinite values
    input_df = input_df.replace(
        [
            float("inf"),
            float("-inf")
        ],
        0
    )

    # Convert all columns to numeric
    input_df = input_df.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Replace missing values
    input_df = input_df.fillna(0)

    return input_df