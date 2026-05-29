import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Business Analytics Dashboard",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📊 Business Analytics & Decision Intelligence Dashboard")
st.markdown("### Sales, Profit & Customer Insights")

# ---------------- LOAD CSV FILE ----------------
df = pd.read_csv("data.csv")

# ---------------- CLEAN COLUMN NAMES ----------------
df.columns = df.columns.str.strip()

# ---------------- DATE CONVERSION ----------------
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

profit_filter = st.sidebar.multiselect(
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
    (df["Profit Class"].isin(profit_filter)) &
    (df["Ship Mode"].isin(ship_filter))
]

# ---------------- KPIs ----------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_margin = filtered_df["Profit Margin"].mean()
total_customers = filtered_df["Customer ID"].nunique()

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Orders", total_orders)
col4.metric("📊 Avg Margin", f"{avg_margin:.2f}%")
col5.metric("👥 Customers", total_customers)

st.markdown("---")

# ---------------- SALES BY REGION ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Sales by Region")

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        text_auto=True
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("💰 Profit by Region")

    region_profit = (
        filtered_df.groupby("Region")["Gross Profit"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        region_profit,
        names="Region",
        values="Gross Profit"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------- MONTHLY SALES TREND ----------------
st.subheader("📈 Monthly Sales Trend")

filtered_df["Month"] = filtered_df["Order Date"].dt.strftime("%b")

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- TOP PRODUCTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values(by="Sales", ascending=False)
        .head(10)
    )

    fig4 = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        color="Sales"
    )

    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.subheader("🚚 Delivery Days Analysis")

    fig5 = px.histogram(
        filtered_df,
        x="Delivery Days",
        nbins=20,
        color="Ship Mode"
    )

    st.plotly_chart(fig5, use_container_width=True)

# ---------------- SALES RANGE ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Sales Range Distribution")

    sales_range = filtered_df["Sales Range"].value_counts().reset_index()
    sales_range.columns = ["Sales Range", "Count"]

    fig6 = px.pie(
        sales_range,
        names="Sales Range",
        values="Count"
    )

    st.plotly_chart(fig6, use_container_width=True)

with col2:
    st.subheader("🚛 Ship Mode Distribution")

    ship_mode = filtered_df["Ship Mode"].value_counts().reset_index()
    ship_mode.columns = ["Ship Mode", "Count"]

    fig7 = px.bar(
        ship_mode,
        x="Ship Mode",
        y="Count",
        color="Ship Mode",
        text_auto=True
    )

    st.plotly_chart(fig7, use_container_width=True)

# ---------------- STATE ANALYSIS ----------------
st.subheader("🗺️ Top States by Sales")

state_sales = (
    filtered_df.groupby("State or Province")["Sales"]
    .sum()
    .reset_index()
    .sort_values(by="Sales", ascending=False)
    .head(15)
)

fig8 = px.bar(
    state_sales,
    x="State or Province",
    y="Sales",
    color="Sales",
    text_auto=True
)

st.plotly_chart(fig8, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.subheader("📋 Dataset Preview")

st.dataframe(filtered_df.head(50))

# ---------------- DOWNLOAD BUTTON ----------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ---------------- INSIGHTS ----------------
st.subheader("🤖 Business Insights")

top_region = region_sales.sort_values(
    by="Sales",
    ascending=False
).iloc[0]["Region"]

top_state = state_sales.iloc[0]["State or Province"]

st.success(f"✅ Highest sales region: {top_region}")

st.success(f"✅ Top performing state: {top_state}")

st.success("✅ Faster shipping modes improve customer satisfaction.")

st.success("✅ High-margin products should receive priority marketing.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### ✅ Developed by Srishti Singh")
