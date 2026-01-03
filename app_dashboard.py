import time
import streamlit as st
import requests
import folium
import pickle
import numpy as np
from streamlit_folium import st_folium

from preprocessing import load_and_preprocess_data
from stress_index import calculate_stress_index

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Nagpur Smart City Dashboard", layout="wide")

st.title("🏙️ Nagpur Smart City Infrastructure Dashboard")

# --------------------------------------------------
# LOAD & PROCESS DATA
# --------------------------------------------------
df = load_and_preprocess_data()
df = calculate_stress_index(df)

st.subheader("📊 Zone-wise Infrastructure Stress Data")
st.dataframe(df)

# --------------------------------------------------
# CITY RISK MAP
# --------------------------------------------------
st.subheader("🗺️ City Risk Map")

m = folium.Map(location=[21.1458, 79.0882], zoom_start=12)

for _, row in df.iterrows():
    if row["risk_level"] == "High":
        color = "red"
    elif row["risk_level"] == "Medium":
        color = "orange"
    else:
        color = "green"

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=12,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"{row['zone']} - {row['risk_level']} Risk"
    ).add_to(m)

st_folium(m, width=800, height=500)

# --------------------------------------------------
# LIVE WEATHER API
# --------------------------------------------------
st.subheader("🌤️ Live Weather – Nagpur")

API_KEY = "2c8402eeecc54d279bc113e8b1b0fab0"  # Your actual API key
CITY = "Nagpur"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url)
    data = response.json()

    if data.get("cod") == 200:
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        st.metric("🌡️ Temperature (°C)", temperature)
        st.metric("💧 Humidity (%)", humidity)
        st.metric("📈 Pressure (hPa)", pressure)
    else:
        st.error("❌ Weather API error – Check API key or city name")
except Exception as e:
    st.error(f"❌ Error fetching weather: {e}")


    # Load trained model
with open("stress_model.pkl", "rb") as f:
    model = pickle.load(f)

# Example: Predict future water usage
# Use last row as current features
last_row = df.iloc[-1]
X_pred = np.array([[last_row["traffic"], last_row["rain"], last_row["complaints"]]])
predicted_water = model.predict(X_pred)[0]

st.subheader("📈 Predicted Water Usage (Next Hour/Day)")
st.metric("💧 Water Usage (L)", round(predicted_water, 2))

# --------------------------------------------------
# AUTO REFRESH
# --------------------------------------------------
st.caption("🔄 Dashboard auto-refreshes every 5 minutes")
time.sleep(300)
st.rerun()
