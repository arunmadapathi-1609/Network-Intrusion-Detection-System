from pathlib import Path
import glob

import pandas as pd

from src.data.preprocess import preprocess_data

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "Data" / "raw"
PROCESSED_DIR = BASE_DIR / "Data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

PROCESSED_FILE = PROCESSED_DIR / "network_intrusion_processed.csv"
SMALL_FILE = PROCESSED_DIR / "network_intrusion_small.csv"

print("Loading raw dataset...")

csv_files = glob.glob(str(RAW_DIR / "*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV files found in Data/raw")

df = pd.concat(
    [pd.read_csv(file, low_memory=False) for file in csv_files],
    ignore_index=True,
)

print(f"Raw Dataset Shape : {df.shape}")

print("Preprocessing dataset...")

df = preprocess_data(df)

df.to_csv(PROCESSED_FILE, index=False)

print(f"Processed Dataset Shape : {df.shape}")

sample_size = {
    "BENIGN": 100000,
    "DoS Hulk": 30000,
    "DDoS": 30000,
    "PortScan": 25000,
    "DoS GoldenEye": 10000,
    "FTP-Patator": 5000,
    "DoS slowloris": 5000,
    "DoS Slowhttptest": 5000,
    "SSH-Patator": 3000,
    "Bot": 2000,
    "Web Attack - Brute Force": 1470,
    "Web Attack - XSS": 652,
    "Web Attack - Sql Injection": 21,
    "Infiltration": 36,
    "Heartbleed": 11,
}

small_df = pd.concat([
    df[df["Label"] == label].sample(
        n=min(size, len(df[df["Label"] == label])),
        random_state=42,
    )
    for label, size in sample_size.items()
])

small_df = small_df.sample(frac=1, random_state=42).reset_index(drop=True)

small_df.to_csv(SMALL_FILE, index=False)

print("\n" + "=" * 60)
print("DATA PREPARATION COMPLETED")
print("=" * 60)
print(f"Processed Dataset : {PROCESSED_FILE}")
print(f"Processed Shape   : {df.shape}")
print(f"Small Dataset     : {SMALL_FILE}")
print(f"Small Shape       : {small_df.shape}")