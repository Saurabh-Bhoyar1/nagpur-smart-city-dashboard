import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import numpy as np

# Load CSV data
df = pd.read_csv("data/nagpur_data.csv")  # Make sure this path exists

# Features (example: traffic, rain, complaints)
X = df[["traffic", "rain", "complaints"]]
y = df["water_usage"]  # Target variable

# Train Linear Regression model
model = LinearRegression()
model.fit(X, y)

# Save the trained model
with open("stress_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("stress_model.pkl created successfully!")
