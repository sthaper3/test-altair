import streamlit as st
import pandas as pd
import altair as alt

st.title("Inside Airbnb: Interactive Dashboard")

# Load data
df = pd.read_csv("listings.csv")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

# Neighborhood dropdown (filters scatterplot only)
neighs = sorted(df['neighbourhood'].dropna().unique())
selected_neigh = st.sidebar.selectbox("Filter Scatterplot by Neighborhood", ["All"] + neighs)

# Price slider (filters scatterplot only)
min_price = int(df['price'].min())
max_price = int(df['price'].max())
price_range = st.sidebar.slider("Price Range (Scatterplot)", min_price, max_price, (min_price, 850))

# Apply filters to scatterplot
scatter_df = df.copy()

if selected_neigh != "All":
    scatter_df = scatter_df[scatter_df['neighbourhood'] == selected_neigh]

scatter_df = scatter_df[
    (scatter_df['price'] >= price_range[0]) &
    (scatter_df['price'] <= price_range[1])
]

# -----------------------------
# SELECTION FOR BAR → BOXPLOT
# -----------------------------
bar_select = alt.selection_single(fields=['neighbourhood'], empty='none')

# -----------------------------
# 1. BAR CHART: Listings by Neighborhood
# -----------------------------
st.header("Listings by Neighborhood (Click a Bar to Filter Boxplot)")

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
# 2. BOXPLOT: Price Distribution for Selected Neighborhood
# -----------------------------
st.header("Price Distribution (Neighborhood Selected from Bar Chart)")

boxplot = (
    alt.Chart(df)
    .mark_boxplot()
    .encode(
        x=alt.X("neighbourhood:N", title="Neighborhood"),
        y=alt.Y("price:Q", title="Price"),
        color="neighbourhood:N",
        tooltip=["neighbourhood", "price"]
    )
    .transform_filter(bar_select)
    .properties(height=300)
)

st.altair_chart(boxplot, use_container_width=True)

# -----------------------------
# 3. SCATTERPLOT: Price vs Number of Reviews
# -----------------------------
st.header("Price vs. Number of Reviews (Filtered by Dropdown + Slider)")

scatter = (
    alt.Chart(scatter_df)
    .mark_circle(size=60, opacity=0.6)
    .encode(
        x=alt.X("price:Q", title="Price"),
        y=alt.Y("number_of_reviews:Q", title="Number of Reviews"),
        color="neighbourhood:N",
        tooltip=["neighbourhood", "price", "number_of_reviews"]
    )
    .properties(height=300)
)

st.altair_chart(scatter, use_container_width=True)





