import streamlit as st
import pandas as pd
import altair as alt

st.title("Basic Newark Airbnb Dashboard (Stable Version)")

df = pd.read_csv("listings.csv")

# Clean price
df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)

# ---------------------------
# 1. BAR CHART — Listings per Neighborhood
# ---------------------------
bar_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X('neighbourhood:N', sort='-y'),
        y='count():Q',
        color='neighbourhood:N',
        tooltip=['neighbourhood', 'count()']
    )
    .properties(width=700, height=400, title="Number of Listings by Neighborhood")
)

st.subheader("Listings by Neighborhood")
st.altair_chart(bar_chart, use_container_width=True)

# ---------------------------
# 2. BOXPLOT — Price Distribution by Neighborhood
# ---------------------------
boxplot = (
    alt.Chart(df)
    .mark_boxplot(size=60)
    .encode(
        y='neighbourhood:N',
        x='price:Q',
        color='neighbourhood:N',
        tooltip=['neighbourhood', 'price']
    )
    .properties(width=700, height=500, title="Price Distribution by Neighborhood")
)

st.subheader("Price Distribution by Neighborhood")
st.altair_chart(boxplot, use_container_width=True)

# ---------------------------
# 3. SCATTERPLOT — Price vs Number of Reviews
# ---------------------------
scatter = (
    alt.Chart(df)
    .mark_circle(size=120, opacity=0.6)
    .encode(
        x='number_of_reviews:Q',
        y='price:Q',
        color='room_type:N',
        tooltip=['name', 'neighbourhood', 'price', 'number_of_reviews']
    )
    .properties(width=900, height=600, title="Price vs Number of Reviews")
)

st.subheader("Price vs Number of Reviews")
st.altair_chart(scatter, use_container_width=True)




