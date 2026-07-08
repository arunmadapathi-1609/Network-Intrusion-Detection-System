import pandas as pd


INPUT_PATH = "data/processed/network_intrusion_processed.csv"

OUTPUT_PATH = "data/demo_network_traffic.csv"


# Load processed dataset

df = pd.read_csv(INPUT_PATH)


print("Original Shape:")
print(df.shape)


print("\nOriginal Distribution:")
print(df["Label"].value_counts())


# -----------------------------
# Select BENIGN traffic
# -----------------------------

benign = df[
    df["Label"] == "BENIGN"
]


benign_sample = benign.sample(
    n=90000,
    random_state=42
)


# -----------------------------
# Select Attack traffic
# -----------------------------

attacks = df[
    df["Label"] != "BENIGN"
]


attack_sample = attacks.sample(
    n=10000,
    random_state=42
)


# -----------------------------
# Combine
# -----------------------------

demo_df = pd.concat(
    [
        benign_sample,
        attack_sample
    ],
    ignore_index=True
)


# Shuffle

demo_df = demo_df.sample(
    frac=1,
    random_state=42
)


# Save

demo_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\nDemo Dataset Created")

print(
    demo_df.shape
)


print("\nNew Distribution:")

print(
    demo_df["Label"].value_counts()
)