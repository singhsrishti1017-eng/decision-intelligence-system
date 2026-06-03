import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Decision Intelligence Dashboard",
    layout="wide"
)

# Title
st.title("Decision Intelligence System")

# Load Data
df = pd.read_excel("Project Data.xlsx")

# Create Calculated Columns
df["Profit Margin"] = df["Gross Profit"] / df["Sales"]

df["Profit Class"] = df["Profit Margin"].apply(
    lambda x: "High Profit" if x >= 0.65 else "Low Profit"
)

# Convert Dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df["Delivery Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# ---------------- SIDEBAR ----------------

st.sidebar.header("User Capabilities")

# Add ALL option
products = ["All"] + sorted(df["Product Name"].dropna().unique().tolist())
regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
ship_modes = ["All"] + sorted(df["Ship Mode"].dropna().unique().tolist())

selected_product = st.sidebar.selectbox(
    "Product",
    products
)

selected_region = st.sidebar.selectbox(
    "Region",
    regions
)

selected_shipmode = st.sidebar.selectbox(
    "Ship Mode",
    ship_modes
)

priority = st.sidebar.slider(
    "Optimization Priority (Speed vs Profit)",
    0,
    100,
    50
)

# ---------------- FILTERING ----------------

filtered_df = df.copy()

if selected_product != "All":
    filtered_df = filtered_df[
        filtered_df["Product Name"] == selected_product
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_shipmode != "All":
    filtered_df = filtered_df[
        filtered_df["Ship Mode"] == selected_shipmode
    ]

# ---------------- KPIs ----------------

st.subheader("Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
avg_margin = filtered_df["Profit Margin"].mean()
avg_delivery = filtered_df["Delivery Days"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Profit Margin",
    f"{avg_margin:.2%}"
)

col4.metric(
    "Avg Delivery Days",
    round(avg_delivery, 2)
)

# ---------------- SALES BY REGION ----------------

st.subheader("Profit by Region")

region_profit = (
    filtered_df.groupby("Region")["Gross Profit"]
    .sum()
    .reset_index()
)

fig_region = px.bar(
    region_profit,
    x="Region",
    y="Gross Profit",
    title="Gross Profit by Region"
)

st.plotly_chart(fig_region, use_container_width=True)

# ---------------- PRODUCT PERFORMANCE ----------------

st.subheader("Top Products")

top_products = (
    filtered_df.groupby("Product Name")["Gross Profit"]
    .sum()
    .reset_index()
    .sort_values(
        by="Gross Profit",
        ascending=False
    )
)

fig_product = px.bar(
    top_products.head(10),
    x="Product Name",
    y="Gross Profit",
    title="Top 10 Products by Profit"
)

st.plotly_chart(fig_product, use_container_width=True)

# ---------------- PROFIT CLASS ----------------

st.subheader("Profit Classification")

profit_class = (
    filtered_df.groupby("Profit Class")
    .size()
    .reset_index(name="Count")
)

fig_profit = px.pie(
    profit_class,
    names="Profit Class",
    values="Count"
)

st.plotly_chart(fig_profit, use_container_width=True)

# ---------------- WHAT IF ANALYSIS ----------------

st.subheader("What-If Scenario Analysis")

increase = st.slider(
    "Increase Sales (%)",
    0,
    100,
    20
)

projected_sales = total_sales * (1 + increase/100)
projected_profit = projected_sales * avg_margin

col5, col6 = st.columns(2)

col5.metric(
    "Projected Sales",
    f"${projected_sales:,.2f}"
)

col6.metric(
    "Projected Profit",
    f"${projected_profit:,.2f}"
)

# ---------------- RECOMMENDATION DASHBOARD ----------------

st.subheader("Recommendation Dashboard")

if avg_margin < 0.55:
    st.error(
        "Recommendation: Improve pricing strategy and reduce discounts."
    )

elif avg_margin < 0.65:
    st.warning(
        "Recommendation: Improve operational efficiency and shipping performance."
    )

else:
    st.success(
        "Recommendation: Maintain current strategy and scale successful products."
    )

# ---------------- RISK PANEL ----------------

st.subheader("Risk & Impact Panel")

risk_df = filtered_df[
    filtered_df["Profit Margin"] < 0.55
]

st.write("High Risk Products")

if len(risk_df) > 0:
    st.dataframe(
        risk_df[
            [
                "Product Name",
                "Region",
                "Sales",
                "Gross Profit",
                "Profit Margin"
            ]
        ]
    )
else:
    st.success("No high-risk products found.")

# ---------------- DATA TABLE ----------------

st.subheader("Detailed Data")

st.dataframe(filtered_df)

# ---------------- FOOTER ----------------

st.markdown("---")
st.write("Decision Intelligence Dashboard | Internship Project")