import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def build_features(df: pd.DataFrame):
    X = df.drop(columns=["Label"])

    y = df["Label"]

    # Encode target labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Save label encoder
    joblib.dump(label_encoder,"models/label_encoder.pkl")

    # Save feature column names
    joblib.dump(X.columns.tolist(),"models/feature_columns.pkl")

    return X, y, label_encoder


def prepare_input(df: pd.DataFrame, feature_columns):

    df.columns = df.columns.str.strip()

    df = df.reindex(columns=feature_columns,fill_value=0)

    return df