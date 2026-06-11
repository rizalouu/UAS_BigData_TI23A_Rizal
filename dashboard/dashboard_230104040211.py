import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Smart Hospital Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #FFFFFF;
}

h1, h2, h3 {
    color: #111111;
    font-weight: bold;
}

[data-testid="stSidebar"] {
    background-color: #F5F7FA;
}

div[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("🏥 Smart Hospital Monitoring System")

st.write(
    "Real-time hospital monitoring dashboard using Spark Big Data and Machine Learning."
)

st.markdown("---")

# =========================
# LOAD DATA
# =========================

base_path = os.path.abspath("output")

patient_total = pd.read_parquet(f"{base_path}/patient_total")
patient_time = pd.read_parquet(f"{base_path}/patient_time")
ml_data = pd.read_parquet(f"{base_path}/ml_data")

# =========================
# SIDEBAR
# =========================

st.sidebar.header("Filter")

room_filter = st.sidebar.selectbox(
    "Select Room",
    patient_total["room"].unique()
)

# =========================
# FILTER DATA
# =========================

filtered_total = patient_total[
    patient_total["room"] == room_filter
]

total_patient = filtered_total["total_patient"].sum()

# =========================
# KPI SECTION
# =========================

st.subheader("Key Performance Indicators")

col1, col2 = st.columns(2)

col1.metric(
    "Total Patients (All)",
    int(patient_total["total_patient"].sum())
)

col2.metric(
    f"Total in {room_filter}",
    int(total_patient)
)

st.markdown("---")

# =========================
# TREND DATA
# =========================

patient_time["start_time"] = patient_time["window"].apply(
    lambda x: x["start"]
)

# FORMAT JAM
patient_time["start_time"] = pd.to_datetime(
    patient_time["start_time"]
).dt.strftime("%H:%M")

trend_filtered = patient_time[
    patient_time["room"] == room_filter
]

trend_filtered = trend_filtered.sort_values("start_time")

# =========================
# LAYOUT 2 COLUMN
# =========================

left_col, right_col = st.columns([2, 1])

# =========================
# CHART
# =========================

with left_col:

    st.subheader("Patient Time Series")

    fig = px.line(
        trend_filtered,
        x="start_time",
        y="patient_trend",
        markers=True,
        title=""
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="black",
        xaxis_title="Time",
        yaxis_title="Total Patients",
        xaxis=dict(type='category')
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# MACHINE LEARNING
# =========================

with right_col:

    st.subheader("AI Prediction")

    X = ml_data[["hour"]]
    y = ml_data["patient_count"]

    model = LinearRegression()
    model.fit(X, y)

    selected_hour = st.slider(
        "Prediction Hour",
        0,
        23,
        12
    )

    future_hour = np.array([[selected_hour]])

    prediction = model.predict(future_hour)

    st.success(
        f"Predicted patient count at hour {selected_hour}:00 is {prediction[0]:.2f}"
    )

# =========================
# BAR CHART
# =========================

st.subheader("Patient Distribution by Room")

room_chart = patient_total.groupby("room")[
    "total_patient"
].sum()

st.bar_chart(room_chart)

# =========================
# TABLE
# =========================

st.subheader("ML Dataset")

st.dataframe(
    ml_data.head(20),
    use_container_width=True
)