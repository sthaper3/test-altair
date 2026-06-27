import streamlit as st
import pandas as pd
import altair as alt

st.title("Inside Airbnb: Interactive Dashboard")

# Load data
df = pd.read_csv("listings.csv")

# Normalize neighborhood names (important for filtering)
df['neighbourhood'] = df['neighbourhood'].astype(str).str.strip()

# -----------------------------
# SIDEBAR FILTERS (for price scatterplot)
# -----------------------------
st.sidebar.header("Filters")

# Neighborhood dropdown
neighs = sorted(df['neighbourhood'].dropna().unique())
selected_neigh = st.sidebar.selectbox("Filter Price Scatterplot by Neighborhood", ["All"] + neighs)

# Price slider
min_price = int(df['price'].min())
max_price = int(df['price'].max())
price_range = st.sidebar.slider("Price Range", min_price, max_price, (min_price, 850))

# Apply filters to price scatterplot
price_scatter_df = df.copy()

if selected_neigh != "All":
    price_scatter_df = price_scatter_df[price_scatter_df['neighbourhood'] == selected_neigh]

price_scatter_df = price_scatter_df[
    (price_scatter_df['price'] >= price_range[0]) &
    (price_scatter_df['price'] <= price_range[1])
]

# -----------------------------
# SELECTION FOR BAR → AVAILABILITY SCATTER
# -----------------------------
bar_select = alt.selection_point(fields=['neighbourhood'], empty='all')

# -----------------------------
# 1. BAR CHART: Listings by Neighborhood
# -----------------------------
st.header("Listings by Neighborhood (Click a Bar to Filter Availability Scatterplot)")

bar_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("neighbourhood:N", sort="-y", title="Neighborhood"),
        y=alt.Y("count():Q", title="Number of Listings"),
        tooltip=["neighbourhood", "count()"],
        color=alt.condition(bar_select, alt.value("steelblue"), alt.value("lightgray"))
    )
    .add_params(bar_select)
    .properties(height=300)
)

st.altair_chart(bar_chart, use_container_width=True)

# -----------------------------
# 2. AVAILABILITY vs REVIEWS (Filtered by Bar Click)
# -----------------------------
st.header("Availability vs Number of Reviews (Neighborhood Selected from Bar Chart)")

availability_scatter = (
    alt.Chart(df)
    .mark_circle(size=60, opacity=0.6)
    .encode(
        x=alt.X("availability_365:Q", title="Availability (Days per Year)"),
        y=alt.Y("number_of_reviews:Q", title="Number of Reviews"),
        color="neighbourhood:N",
        tooltip=["neighbourhood", "availability_365", "number_of_reviews"]
    )
    .transform_filter(bar_select)
    .properties(height=300)
)

st.altair_chart(availability_scatter, use_container_width=True)

# -----------------------------
# 3. PRICE vs REVIEWS (Filtered by Dropdown + Slider)
# -----------------------------
st.header("Price vs Number of Reviews (Filtered by Dropdown + Slider)")

price_scatter = (
    alt.Chart(price_scatter_df)
    .mark_circle(size=60, opacity=0.6)
    .encode(
        x=alt.X("price:Q", title="Price"),
        y=alt.Y("number_of_reviews:Q", title="Number of Reviews"),
        color="neighbourhood:N",
        tooltip=["neighbourhood", "price", "number_of_reviews"]
    )
    .properties(height=300)
)

st.altair_chart(price_scatter, use_container_width=True)






