import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(page_title="EDA Dashboard", layout="wide")
st.title("📊 Python Session Interval EDA")

# Sidebar options
st.sidebar.header("Data Controls")

# Toggle to use sample data or upload
use_sample = st.toggle("Use sample data", value=False)
file_path = None

if not use_sample:
    uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    file_path = st.sidebar.text_input("Or enter local file path")

if use_sample:
    # Sample dataset
    data = pd.DataFrame({
        "Entered Interval": ["11:00 - 11:15", "10:45 - 11:00", "11:30 - 11:45", "12:15 - 12:30"],
        "Exited Interval": ["13:45 - 14:00", "12:00 - 12:15", "12:30 - 12:45", "13:00 - 13:15"],
        "Entry Count": [10, 5, 8, 12],
        "Time in Session": ["30 - 59", "0 - 29", "60 - 89", "30 - 59"],
        "OTO/Non OTO": ["Non OTO", "OTO", "Non OTO", "OTO"],
        "Workshop Date": ["01/15/2025", "01/16/2025", "01/16/2025", "01/17/2025"]
    })
else:
    if uploaded_file:
        if uploaded_file.name.endswith("csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
    elif file_path and os.path.exists(file_path):
        if file_path.endswith("csv"):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)
    else:
        st.warning("Please upload a file, enter a valid file path, or use sample data.")
        st.stop()

# Convert dates safely
try:
    data["Workshop Date"] = pd.to_datetime(data["Workshop Date"], errors="coerce", infer_datetime_format=True)
except Exception:
    st.warning("Date parsing issue: Please ensure Workshop Date is in a standard format (e.g., MM/DD/YYYY).")

# Sidebar filters
col_options = data.columns.tolist()
x_axis = st.sidebar.selectbox("Select X-axis", options=col_options, index=0)
y_axis = st.sidebar.selectbox("Select Y-axis", options=col_options, index=2)
color_opt = st.sidebar.selectbox("Color by", options=[None] + col_options, index=0)

# KPIs
with st.container():
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Records", len(data))
    kpi2.metric("Unique Sessions", data["Time in Session"].nunique())
    kpi3.metric("Unique Dates", data["Workshop Date"].nunique())

# --- Visualizations ---

# 1. Scatter Plot
st.subheader("Scatter Plot")
fig_scatter = px.scatter(data, x=x_axis, y=y_axis, color=color_opt, size="Entry Count", hover_data=data.columns)
st.plotly_chart(fig_scatter, use_container_width=True)

# 2. Bar Chart for Time in Session
st.subheader("Bar Chart - Time in Session")
fig_bar = px.bar(data, x="Time in Session", y="Entry Count", color=color_opt, barmode="group")
st.plotly_chart(fig_bar, use_container_width=True)

# 3. Pie Chart for OTO/Non OTO
st.subheader("Pie Chart - OTO vs Non OTO")
fig_pie = px.pie(data, names="OTO/Non OTO", values="Entry Count", hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)

# 4. Line Chart for Workshop Date
st.subheader("Line Chart - Workshop Date vs Entry Count")
fig_line = px.line(data.groupby("Workshop Date")["Entry Count"].sum().reset_index(),
                   x="Workshop Date", y="Entry Count", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# 5. Box Plot for Distribution
st.subheader("Box Plot - Distribution of Entry Count")
fig_box = px.box(data, y="Entry Count", color="Time in Session")
st.plotly_chart(fig_box, use_container_width=True)

st.success("Use sidebar to control visualizations.")
