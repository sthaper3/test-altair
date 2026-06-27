import streamlit as st
import pandas as pd
import altair as alt

st.title("Airbnb Listings in Newark, NJ")

df = pd.read_csv("listings.csv")

df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)

# Sidebar filters
st.sidebar.header("Filters")

room_types = df['room_type'].dropna().unique().tolist()
selected_room = st.sidebar.selectbox("Room Type", ["All"] + room_types)

min_price, max_price = int(df['price'].min()), int(df['price'].max())
price_range = st.sidebar.slider("Price Range", min_price, max_price, (min_price, max_price))

filtered = df.copy()

if selected_room != "All":
    filtered = filtered[filtered['room_type'] == selected_room]

filtered = filtered[(filtered['price'] >= price_range[0]) & (filtered['price'] <= price_range[1])]

# Selections (v4-compatible)
map_select = alt.selection_point(fields=['neighbourhood'], empty='all')
box_select = alt.selection_point(fields=['neighbourhood'], empty='all')

# ---------------------------
# MAP
# ---------------------------
map_chart = (
    alt.Chart(filtered)
    .mark_circle(size=60, opacity=0.5)
    .encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        color=alt.Color('price:Q', scale=alt.Scale(scheme='viridis')),
        tooltip=['name', 'neighbourhood', 'price', 'room_type'],
        opacity=alt.condition(map_select, alt.value(1), alt.value(0.3))
    )
    .add_selection(map_select)
    .properties(width=700, height=400, title="Map of Listings")
)

st.subheader("Map of Listings")
st.altair_chart(map_chart, use_container_width=True)

# ---------------------------
# BOXPLOT
# ---------------------------
boxplot = (
    alt.Chart(filtered)
    .mark_boxplot()
    .encode(
        x='neighbourhood:N',
        y='price:Q',
        color='neighbourhood:N',
        opacity=alt.condition(box_select, alt.value(1), alt.value(0.4)),
        tooltip=['neighbourhood', 'price']
    )
    .add_selection(box_select)
    .transform_filter(map_select)
    .properties(width=700, height=400, title="Price Distribution by Neighborhood")
)

st.subheader("Price Distribution by Neighborhood")
st.altair_chart(boxplot, use_container_width=True)

# ---------------------------
# SCATTERPLOT
# ---------------------------
scatter = (
    alt.Chart(filtered)
    .mark_circle(size=70, opacity=0.6)
    .encode(
        x='number_of_reviews:Q',
        y='price:Q',
        color='room_type:N',
        tooltip=['name', 'neighbourhood', 'price', 'number_of_reviews'],
        opacity=alt.condition(box_select, alt.value(1), alt.value(0.2))
    )
    .transform_filter(map_select)
    .transform_filter(box_select)
    .properties(width=700, height=400, title="Price vs Number of Reviews")
)

st.subheader("Price vs Number of Reviews")
st.altair_chart(scatter, use_container_width=True)
