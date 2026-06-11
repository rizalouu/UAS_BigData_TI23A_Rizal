import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="Smart Retail Visitor Prediction",
    layout="wide"
)

st.title("🛍️ Smart Retail Visitor Prediction System")
st.markdown("---")

# =====================================
# LOAD DATA
# =====================================

total_df = pd.read_parquet("data/serving/visitor_total")
time_df = pd.read_parquet("data/serving/visitor_time")
ml_df = pd.read_parquet("data/serving/ml_visitor")

# =====================================
# SIDEBAR
# =====================================

zone = st.sidebar.selectbox(
    "Pilih Zona",
    sorted(ml_df["zone"].unique())
)

# =====================================
# KPI
# =====================================

zone_total = total_df[
    total_df["zone"] == zone
]

total_visitors = int(
    zone_total["total_visitors"].sum()
)

avg_visitors = int(
    ml_df[
        ml_df["zone"] == zone
    ]["visitor_count"].mean()
)

max_visitors = int(
    ml_df[
        ml_df["zone"] == zone
    ]["visitor_count"].max()
)

records = len(
    ml_df[
        ml_df["zone"] == zone
    ]
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Visitors",
    f"{total_visitors:,}"
)

c2.metric(
    "Average Visitors",
    f"{avg_visitors:,}"
)

c3.metric(
    "Peak Visitors",
    f"{max_visitors:,}"
)

c4.metric(
    "Records",
    f"{records:,}"
)

st.markdown("---")

# =====================================
# CHARTS
# =====================================

left, right = st.columns(2)

with left:

    st.subheader("Visitor Trend")

    trend = time_df[
        time_df["zone"] == zone
    ]

    fig = px.bar(
        trend,
        x="minute_block",
        y="visitor_count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Visitor Distribution")

    fig2 = px.histogram(
        ml_df[
            ml_df["zone"] == zone
        ],
        x="visitor_count"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.markdown("---")

# =====================================
# MACHINE LEARNING
# =====================================

st.subheader("AI Visitor Prediction")

zone_ml = ml_df[
    ml_df["zone"] == zone
]

X = zone_ml[["hour"]]
y = zone_ml["visitor_count"]

model = LinearRegression()
model.fit(X, y)

hour_predict = st.slider(
    "Pilih Jam Prediksi",
    0,
    23,
    12
)

prediction = model.predict(
    np.array([[hour_predict]])
)

st.success(
    f"Prediksi jumlah pengunjung pada jam {hour_predict}:00 adalah {int(prediction[0])} orang"
)

st.markdown("---")

st.subheader("Dataset Preview")

st.dataframe(
    zone_ml.head(20),
    use_container_width=True
)