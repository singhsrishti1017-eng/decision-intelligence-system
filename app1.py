import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Business Analytics Dashboard",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📊 Business Analytics & Decision Intelligence Dashboard")
st.markdown("### AI-Based Sales, Profit & Regional Performance Analytics")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("data.xlsx")

# ---------------- CLEAN COLUMN NAMES ----------------
df.columns = df.columns.str.strip()

# ---------------- DATE CONVERSION ----------------
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Dashboard Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)
ship_filter = st.sidebar.multiselect(
    "Select Ship Mode",
    options=df["Ship Mode"].unique(),
    default=df["Ship Mode"].unique()
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["Region"].isin(region_filter)) &
    (df["Profit Class"].isin(category_filter)) &
    (df["Ship Mode"].isin(ship_filter))
]

# ---------------- KPIs ----------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_margin = filtered_df["Profit Margin"].mean()

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("Total Profit", f"₹ {total_profit:,.0f}")
col3.metric("Total Orders", total_orders)
col4.metric("Avg Profit Margin", f"{avg_margin:.2f}%")

st.markdown("---")

# ---------------- SALES BY REGION ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Sales by Region")

    region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()

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

    region_profit = filtered_df.groupby("Region")["Gross Profit"].sum().reset_index()

    fig2 = px.pie(
        region_profit,
        names="Region",
        values="Gross Profit"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------- MONTHLY SALES TREND ----------------
st.subheader("📈 Monthly Sales Trend")

filtered_df["Month"] = filtered_df["Order Date"].dt.strftime("%b")

month_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()

fig3 = px.line(
    month_sales,
    x="Month",
    y="Sales",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- TOP PRODUCTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Products by Sales")

    top_products = filtered_df.groupby("Product Name")["Sales"].sum().reset_index()

    top_products = top_products.sort_values(
        by="Sales",
        ascending=False
    ).head(10)

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
    st.subheader("💳 Ship Mode Distribution")

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
st.subheader("🗺️ State-wise Sales Performance")

state_sales = filtered_df.groupby("State or Province")["Sales"].sum().reset_index()

state_sales = state_sales.sort_values(
    by="Sales",
    ascending=False
).head(15)

fig8 = px.bar(
    state_sales,
    x="State or Province",
    y="Sales",
    color="Sales",
    text_auto=True
)

st.plotly_chart(fig8, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.subheader("📋 Transaction Data")

st.dataframe(filtered_df)

# ---------------- DOWNLOAD OPTION ----------------
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv',
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "### ✅ Developed for Business Analytics & Decision Intelligence Project"
)
