import streamlit as st
import pandas as pd
import altair as alt

st.title("Interactive Dashboard For Airbnb Listings in Newark, NJ")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("listings.csv")   

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

# Neighborhood dropdown
neighborhoods = sorted(df['neighbourhood'].dropna().unique())
selected_neigh = st.sidebar.selectbox("Neighborhood", ["All"] + neighborhoods)

# Price slider
min_price = int(df['price'].min())
max_price = int(df['price'].max())
price_range = st.sidebar.slider("Price Range", min_price, max_price, (min_price, 850))

# Review slider
min_reviews = int(df['number_of_reviews'].min())
max_reviews = int(df['number_of_reviews'].max())
review_range = st.sidebar.slider("Number of Reviews", min_reviews, max_reviews, (0, 500))

# Apply filters
filtered = df.copy()

if selected_neigh != "All":
    filtered = filtered[filtered['neighbourhood'] == selected_neigh]

filtered = filtered[
    (filtered['price'] >= price_range[0]) &
    (filtered['price'] <= price_range[1]) &
    (filtered['number_of_reviews'] >= review_range[0]) &
    (filtered['number_of_reviews'] <= review_range[1])
]

# -----------------------------
# LINKED SELECTION (BRUSH)
# -----------------------------
brush = alt.selection_interval(encodings=['x', 'y'])

# -----------------------------
# 1. BAR CHART: Listings by Neighborhood
# -----------------------------
st.header("Number of Listings by Neighborhood")

bar_chart = (
    alt.Chart(filtered)
    .mark_bar()
    .encode(
        x=alt.X("neighbourhood:N", sort="-y", title="Neighborhood"),
        y=alt.Y("count():Q", title="Number of Listings"),
        tooltip=["neighbourhood", "count()"]
    )
    .properties(height=300)
)

st.altair_chart(bar_chart, use_container_width=True)

# -----------------------------
# 2. BOXPLOT: Price Distribution Across Neighborhoods
# -----------------------------
st.header("Price Distribution Across Neighborhoods")

boxplot = (
    alt.Chart(filtered)
    .mark_boxplot()
    .encode(
        x=alt.X("neighbourhood:N", title="Neighborhood"),
        y=alt.Y("price:Q", title="Price"),
        color="neighbourhood:N",
        tooltip=["neighbourhood", "price"]
    )
    .transform_filter(brush)
    .properties(height=300)
)

st.altair_chart(boxplot, use_container_width=True)

# -----------------------------
# 3. SCATTERPLOT: Price vs Number of Reviews (BRUSHABLE)
# -----------------------------
st.header("Price vs. Number of Reviews")

scatter = (
    alt.Chart(filtered)
    .mark_circle(size=60, opacity=0.6)
    .encode(
        x=alt.X("price:Q", title="Price"),
        y=alt.Y("number_of_reviews:Q", title="Number of Reviews"),
        color="neighbourhood:N",
        tooltip=["neighbourhood", "price", "number_of_reviews"]
    )
    .add_params(brush)
    .properties(height=300)
)

st.altair_chart(scatter, use_container_width=True)




