import numpy as np
import pandas as pd


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:

    # Remove leading/trailing spaces
    df.columns = df.columns.str.strip()

    # Remove negative flow duration
    if "Flow Duration" in df.columns:
        df = df[df["Flow Duration"] >= 0]

    # Replace infinite values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Remove missing values
    df.dropna(inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df


def split_features_target(df: pd.DataFrame):
    
    X = df.drop("Label", axis=1)
    y = df["Label"]

    return X, y


def preprocess_input(df: pd.DataFrame, feature_columns):

    # Remove spaces
    df.columns = df.columns.str.strip()

    # Arrange columns exactly like training
    df = df.reindex(columns=feature_columns, fill_value=0)

    return df