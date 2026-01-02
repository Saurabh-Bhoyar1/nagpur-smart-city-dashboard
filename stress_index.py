def calculate_stress_index(df):
    # Weight for each parameter
    weights = {
        "traffic": 0.3,
        "rain": 0.2,
        "complaints": 0.3,
        "water_usage": 0.2
    }

    # Stress Index calculation
    df["stress_index"] = (
        df["traffic"] * weights["traffic"] +
        df["rain"] * weights["rain"] +
        df["complaints"] * weights["complaints"] +
        df["water_usage"] * weights["water_usage"]
    )

    # Risk classification
    def classify_risk(value):
        if value < 40:
            return "Low"
        elif value < 70:
            return "Medium"
        else:
            return "High"

    df["risk_level"] = df["stress_index"].apply(classify_risk)

    return df
