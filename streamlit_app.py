import streamlit as st
import pandas as pd
import altair as alt

st.title("Inside Airbnb: Interactive Dashboard")

# Load data
df = pd.read_csv("listings.csv")
df['neighbourhood'] = df['neighbourhood'].astype(str).str.strip()

# Sidebar filters (unchanged)
st.sidebar.header("Filters")
neighs = sorted(df['neighbourhood'].dropna().unique())
selected_neigh = st.sidebar.selectbox("Filter Price Scatterplot by Neighborhood", ["All"] + neighs)

min_price = int(df['price'].min())
max_price = int(df['price'].max())
price_range = st.sidebar.slider("Price Range", min_price, max_price, (min_price, 850))

price_scatter_df = df.copy()
if selected_neigh != "All":
    price_scatter_df = price_scatter_df[price_scatter_df['neighbourhood'] == selected_neigh]
 price_scatter_df = price_scatter_df[
(price_scatter_df['price'] >= price_range[0]) &
(price_scatter_df['price'] <= price_range[1])
]

# -----------------------------
# INTERACTIVE SELECTION (Altair 4)
# -----------------------------
bar_select = alt.selection_single(fields=['neighbourhood'], empty='all')

# -----------------------------
# 1. BAR CHART
# -----------------------------
st.header("Listings by Neighborhood (Click a bar to filter the scatterplot below)")

bar_chart = (
alt.Chart(df)
.mark_bar()
.encode(
x=alt.X("neighbourhood:N", sort="-y", title="Neighborhood"),
y=alt.Y("count():Q", title="Number of Listings"),
tooltip=["neighbourhood", "count()"],
color=alt.condition(bar_select, alt.value("steelblue"), alt.value("lightgray"))
)
.add_selection(bar_select) # <-- Changed from add_params to add_selection
.properties(height=300)
)
st.altair_chart(bar_chart, use_container_width=True)

# -----------------------------
# 2. AVAILABILITY vs REVIEWS (filtered by bar click)
# -----------------------------
st.header("Availability vs Number of Reviews (filtered by clicked bar)")

availability_scatter = (
alt.Chart(df)
.mark_circle(size=60, opacity=0.6)
.encode(
x=alt.X("availability_365:Q", title="Availability (days per year)"),
y=alt.Y("number_of_reviews:Q", title="Number of Reviews"),
color="neighbourhood:N",
tooltip=["neighbourhood", "availability_365", "number_of_reviews"]
)
.transform_filter(bar_select)
.properties(height=300)
)
st.altair_chart(availability_scatter, use_container_width=True)

# -----------------------------
# 3. PRICE vs REVIEWS (unchanged)
# -----------------------------
st.header("Price vs Number of Reviews (filtered by dropdown & slider)")

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






