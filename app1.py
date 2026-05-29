import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Business Analytics Dashboard",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📊 Business Analytics & Decision Intelligence Dashboard")
st.markdown("### Sales, Profitability & Customer Insights System")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("your_file_name.xlsx")

# ---------------- DATE CONVERSION ----------------
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Dashboard Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Profit Class",
    options=df["Profit Class"].unique(),
    default=df["Profit Class"].unique()
)

ship_filter = st.sidebar.multiselect(
    "Select Ship Mode",
    options=df["Ship Mode"].unique(),
    default=df["Ship Mode"].unique()
)

# ---------------- FILTERED DATA ----------------
filtered_df = df[
    (df["Region"].isin(region_filter)) &
    (df["Profit Class"].isin(category_filter)) &
    (df["Ship Mode"].isin(ship_filter))
]

# ---------------- KPI SECTION ----------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_margin = filtered_df["Profit Margin"].mean()
total_customers = filtered_df["Customer ID"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Orders", total_orders)
col4.metric("📊 Avg Profit Margin", f"{avg_margin:.2f}%")
col5.metric("👥 Customers", total_customers)

st.markdown("---")

# ---------------- SALES BY REGION ----------------
st.subheader("🌍 Sales by Region")

sales_region = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig1 = px.bar(
    sales_region,
    x="Region",
    y="Sales",
    color="Region",
    title="Regional Sales Analysis"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- PROFIT BY STATE ----------------
st.subheader("🏙️ Profit by State")

profit_state = (
    filtered_df.groupby("State or Province")["Gross Profit"]
    .sum()
    .reset_index()
    .sort_values(by="Gross Profit", ascending=False)
    .head(10)
)

fig2 = px.bar(
    profit_state,
    x="State or Province",
    y="Gross Profit",
    color="Gross Profit",
    title="Top Profitable States"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- SALES TREND ----------------
st.subheader("📅 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig3 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- SHIP MODE DISTRIBUTION ----------------
st.subheader("🚚 Ship Mode Distribution")

ship_data = filtered_df["Ship Mode"].value_counts().reset_index()
ship_data.columns = ["Ship Mode", "Count"]

fig4 = px.pie(
    ship_data,
    names="Ship Mode",
    values="Count",
    title="Shipping Preferences"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- TOP PRODUCTS ----------------
st.subheader("🏆 Top Selling Products")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .reset_index()
    .sort_values(by="Sales", ascending=False)
    .head(10)
)

fig5 = px.bar(
    top_products,
    x="Product Name",
    y="Sales",
    color="Sales",
    title="Top 10 Products"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------- PROFIT CLASS ----------------
st.subheader("📊 Profit Class Analysis")

profit_class = (
    filtered_df.groupby("Profit Class")["Gross Profit"]
    .sum()
    .reset_index()
)

fig6 = px.bar(
    profit_class,
    x="Profit Class",
    y="Gross Profit",
    color="Profit Class",
    title="Profit Category Performance"
)

st.plotly_chart(fig6, use_container_width=True)

# ---------------- DELIVERY ANALYSIS ----------------
st.subheader("⏱️ Delivery Days Analysis")

fig7 = px.histogram(
    filtered_df,
    x="Delivery Days",
    nbins=20,
    title="Delivery Time Distribution"
)

st.plotly_chart(fig7, use_container_width=True)

# ---------------- SALES RANGE ANALYSIS ----------------
st.subheader("💵 Sales Range Distribution")

sales_range = filtered_df["Sales Range"].value_counts().reset_index()
sales_range.columns = ["Sales Range", "Count"]

fig8 = px.pie(
    sales_range,
    names="Sales Range",
    values="Count",
    title="Sales Range Distribution"
)

st.plotly_chart(fig8, use_container_width=True)

# ---------------- CUSTOMER TABLE ----------------
st.subheader("📋 Detailed Dataset")

st.dataframe(filtered_df.head(50))

# ---------------- INSIGHTS SECTION ----------------
st.subheader("🤖 Business Insights")

highest_region = sales_region.sort_values(
    by="Sales",
    ascending=False
).iloc[0]["Region"]

highest_profit_state = profit_state.iloc[0]["State or Province"]

st.success(f"✅ Highest sales generated from: {highest_region}")

st.success(f"✅ Most profitable state: {highest_profit_state}")

st.success("✅ Customers prefer faster shipping methods.")

st.success("✅ High profit products should receive priority marketing.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### ✅ Developed by Srishti Singh")
st.markdown("Business Analytics & Decision Intelligence Project")
