# =====================================
# REAL-TIME DASHBOARD (STREAMLIT)
# =====================================

import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(layout="wide")

st.title("E-Commerce Real-Time Dashboard")
st.subheader("Streaming Analytics - Big Data")

DATA_PATH = "data/serving/stream"

# ============================
# LOAD DATA
# ============================
def load_data():
    try:
        files = [f for f in os.listdir(DATA_PATH) if f.endswith(".parquet")]
        if not files:
            return pd.DataFrame()

        df_list = []
        for f in files:
            df = pd.read_parquet(os.path.join(DATA_PATH, f))
            df_list.append(df)

        return pd.concat(df_list, ignore_index=True)

    except:
        return pd.DataFrame()

# ============================
# AUTO REFRESH LOOP
# ============================
placeholder = st.empty()

while True:
    with placeholder.container():

        df = load_data()

        if df.empty:
            st.warning("Waiting for streaming data...")
        else:
            # ============================
            # KPI (4 METRICS)
            # ============================
            total_revenue = df["total_amount"].sum()
            total_transactions = len(df)
            total_quantity = df["quantity"].sum()
            avg_transaction = total_revenue / total_transactions if total_transactions > 0 else 0

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Revenue", f"Rp {total_revenue:,.0f}")
            col2.metric("Total Transactions", total_transactions)
            col3.metric("Avg Transaction", f"Rp {avg_transaction:,.0f}")
            col4.metric("Total Quantity", total_quantity)

            st.divider()

            # ============================
            # REVENUE TREND
            # ============================
            st.subheader("Revenue Trend")

            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["minute"] = df["timestamp"].dt.strftime("%H:%M")

            trend_df = df.groupby("minute")["total_amount"].sum()

            st.line_chart(trend_df)

            st.divider()

            # ============================
            # Revenue per City
            # ============================
            st.subheader("Revenue per City")
            city_df = df.groupby("city")["total_amount"].sum().sort_values(ascending=False)
            st.bar_chart(city_df)

            # ============================
            # Top Products
            # ============================
            st.subheader("Top Products")
            product_df = df.groupby("product")["quantity"].sum().sort_values(ascending=False)
            st.bar_chart(product_df)

            # ============================
            # Live Transactions
            # ============================
            st.subheader("Live Transactions")
            st.dataframe(df.tail(10))

    time.sleep(5)