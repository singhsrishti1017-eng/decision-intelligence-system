import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Decision Intelligence Dashboard", layout="wide")

# Title
st.title("Decision Intelligence System")

# Load data
df = pd.read_excel("Cleaned_Data.xlsx")

# Sidebar Filters
st.sidebar.header("User Capabilities")

product = st.sidebar.selectbox(
    "Select Product",
    df["Product Name"].unique()
)

region = st.sidebar.selectbox(
    "Select Region",
    df["Region"].unique()
)

ship_mode = st.sidebar.selectbox(
    "Select Ship Mode",
    df["Ship Mode"].unique()
)

priority = st.sidebar.slider(
    "Optimization Priority (Speed vs Profit)",
    0, 100, 50
)

# Filter data
filtered_df = df[
    (df["Product Name"] == product) &
    (df["Region"] == region) &
    (df["Ship Mode"] == ship_mode)
]

# KPIs
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
avg_margin = filtered_df["Profit Margin"].mean()

# KPI Display
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", round(total_sales,2))
col2.metric("Total Profit", round(total_profit,2))
col3.metric("Average Margin", round(avg_margin,2))

# Profit Chart
st.subheader("Profit by Product")

fig = px.bar(
    filtered_df,
    x="Product Name",
    y="Gross Profit",
    color="Profit Class"
)

st.plotly_chart(fig, use_container_width=True)

# Scenario Analysis
st.subheader("What-If Scenario Analysis")

sales_increase = st.slider(
    "Increase Sales %",
    0, 100, 20
)

new_sales = total_sales * (1 + sales_increase/100)
new_profit = new_sales * avg_margin

st.write("Projected Sales:", round(new_sales,2))
st.write("Projected Profit:", round(new_profit,2))

# Recommendation Engine
st.subheader("Recommendation Dashboard")

if avg_margin < 0.55:
    st.error("High Risk Product - Reduce Discounts")
elif avg_margin < 0.65:
    st.warning("Moderate Margin - Improve Efficiency")
else:
    st.success("High Profit Product - Maintain Strategy")

# Risk Panel
st.subheader("Risk & Impact Panel")

risk_products = df[df["Profit Margin"] < 0.55]

st.dataframe(
    risk_products[
        ["Product Name","Region","Gross Profit","Profit Margin"]
    ]
)