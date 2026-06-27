import streamlit as st
import pandas as pd
import altair as alt

st.title("Airbnb Listings in Newark, NJ")

df = pd.read_csv("listings.csv")

# Clean price
df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("Filters")

# Room type filter
room_types = df['room_type'].dropna().unique().tolist()
selected_room = st.sidebar.selectbox("Room Type", ["All"] + room_types)

# Price slider
min_price, max_price = int(df['price'].min()), int(df['price'].max())
price_range = st.sidebar.slider("Price Range", min_price, max_price, (min_price, max_price))

# Apply filters
filtered = df.copy()

if selected_room != "All":
    filtered = filtered[filtered['room_type'] == selected_room]

filtered = filtered[
    (filtered['price'] >= price_range[0]) &
    (filtered['price'] <= price_range[1])
]

# ---------------------------
# INTERACTIVITY: selection shared across bar + scatter
# ---------------------------
neigh_select = alt.selection_single(fields=['neighbourhood'], empty='all')

# ---------------------------
# 1. BAR CHART — Listings per Neighborhood
# ---------------------------
bar_chart = (
    alt.Chart(filtered)
    .mark_bar()
    .encode(
        x=alt.X('neighbourhood:N', sort='-y',
                axis=alt.Axis(title='Neighborhood')),
        y=alt.Y('count():Q',
                axis=alt.Axis(title='Number of Listings')),
        color=alt.condition(
            neigh_select,
            alt.Color('neighbourhood:N', scale=alt.Scale(scheme='category20')),
            alt.value('lightgray')
        ),
        tooltip=['neighbourhood', 'count()']
    )
    .add_selection(neigh_select)
    .properties(width=700, height=300, title="Number of Listings by Neighborhood")
)

# ---------------------------
# 2. SCATTERPLOT — Price vs Number of Reviews (filtered by selection)
# ---------------------------
scatter = (
    alt.Chart(filtered)
    .mark_circle(size=120, opacity=0.6)
    .encode(
    x=alt.X('number_of_reviews:Q',
            axis=alt.Axis(title='Number of Reviews')),
    y=alt.Y('price:Q',
            axis=alt.Axis(title='Price')),
    color='room_type:N',
    tooltip=['name', 'neighbourhood', 'price', 'number_of_reviews']
)

    .transform_filter(neigh_select)
    .properties(width=700, height=400, title="Price vs Number of Reviews")
)

# ---------------------------
# COMBINE BAR + SCATTER SO SELECTION WORKS
# ---------------------------
bar_scatter = alt.vconcat(bar_chart, scatter)

st.subheader("Listings and Reviews by Neighborhood")
st.altair_chart(bar_scatter, use_container_width=True)

# ---------------------------
# 3. BOXPLOT — Price Distribution by Neighborhood (independent)
# ---------------------------
boxplot = (
    alt.Chart(filtered)
    .mark_boxplot(size=60)
    .encode(
    y=alt.Y('neighbourhood:N',
            axis=alt.Axis(title='Neighborhood')),
    x=alt.X('price:Q',
            axis=alt.Axis(title='Price')),
    color='neighbourhood:N',
    tooltip=['neighbourhood', 'price']
)

    .properties(width=700, height=500, title="Price Distribution by Neighborhood")
)

st.subheader("Price Distribution by Neighborhood")
st.altair_chart(boxplot, use_container_width=True)






