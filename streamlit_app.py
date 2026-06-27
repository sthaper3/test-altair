import streamlit as st
import pandas as pd
import altair as alt

st.title("Basic Newark Airbnb Dashboard (No Interactivity Yet)")

df = pd.read_csv("listings.csv")

# Clean price
df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)

# ---------------------------
# 1. MAP
# ---------------------------
map_chart = (
    alt.Chart(df)
    .mark_circle(size=40, opacity=0.5)
    .encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        color=alt.Color('price:Q', scale=alt.Scale(scheme='viridis')),
        tooltip=['name', 'neighbourhood', 'price', 'room_type']
    )
    .properties(width=700, height=400, title="Map of Listings")
)

st.subheader("Map of Listings")
st.altair_chart(map_chart, use_container_width=True)

# ---------------------------
# 2. BOXPLOT
# ---------------------------
boxplot = (
    alt.Chart(df)
    .mark_boxplot()
    .encode(
        x='neighbourhood:N',
        y='price:Q',
        color='neighbourhood:N',
        tooltip=['neighbourhood', 'price']
    )
    .properties(width=700, height=400, title="Price Distribution by Neighborhood")
)

st.subheader("Price Distribution by Neighborhood")
st.altair_chart(boxplot, use_container_width=True)

# ---------------------------
# 3. SCATTERPLOT
# ---------------------------
scatter = (
    alt.Chart(df)
    .mark_circle(size=60, opacity=0.6)
    .encode(
        x='number_of_reviews:Q',
        y='price:Q',
        color='room_type:N',
        tooltip=['name', 'neighbourhood', 'price', 'number_of_reviews']
    )
    .properties(width=700, height=400, title="Price vs Number of Reviews")
)

st.subheader("Price vs Number of Reviews")
st.altair_chart(scatter, use_container_width=True)


