import time
import streamlit as st
from preprocessing import load_and_preprocess_data
from stress_index import calculate_stress_index
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Nagpur Smart City Dashboard", layout="wide")
st.title("Nagpur Smart City Infrastructure Dashboard")

# Load and process data
df = load_and_preprocess_data()
df = calculate_stress_index(df)

# Show table
st.subheader("Zone-wise Infrastructure Stress Data")
st.dataframe(df)

# Create map
st.subheader("City Risk Map")
m = folium.Map(location=[21.1458, 79.0882], zoom_start=12)

# Add zone markers
for _, row in df.iterrows():
    if row["risk_level"] == "High":
        color = "red"
    elif row["risk_level"] == "Medium":
        color = "orange"
    else:
        color = "green"

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=15,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"{row['zone']} - {row['risk_level']} Risk"
    ).add_to(m)

# Show map
st_folium(m, width=800, height=500)

st.caption("Dashboard auto-refreshes every 15 seconds")
time.sleep(15)
st.rerun()

