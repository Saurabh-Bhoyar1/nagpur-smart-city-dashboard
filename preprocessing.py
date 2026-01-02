import pandas as pd

def load_and_preprocess_data():
    # Load CSV file
    df = pd.read_csv("data/nagpur_data.csv")

    # Normalize numeric columns to 0–100 scale
    numeric_cols = ["traffic", "rain", "complaints", "water_usage"]
    for col in numeric_cols:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min()) * 100

    # Add Nagpur zone coordinates (approximate)
    zone_coordinates = {
        "Central": (21.1458, 79.0882),
        "East": (21.1490, 79.1000),
        "West": (21.1400, 79.0700)
    }

    df["latitude"] = df["zone"].map(lambda z: zone_coordinates[z][0])
    df["longitude"] = df["zone"].map(lambda z: zone_coordinates[z][1])

    return df
