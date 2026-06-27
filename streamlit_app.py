
import streamlit as st
import pandas as pd
import altair as alt

st.title("Interactive University Donations Dashboard")

# -------------------------
# Load data
# -------------------------
df = pd.read_csv("university-donations.csv")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

# Gift Amount slider
amount_range = st.sidebar.slider(
    "Select Gift Amount Range",
    min_value=0,
    max_value=int(df["Gift Amount"].max()),
    value=(0, int(df["Gift Amount"].max()))
)

# College dropdown
college_filter = st.sidebar.selectbox(
    "Filter by College",
    options=["All"] + sorted(df["College"].dropna().unique().tolist())
)

# Apply filters
df_filtered = df[df["Gift Amount"].between(amount_range[0], amount_range[1])]

if college_filter != "All":
    df_filtered = df_filtered[df_filtered["College"] == college_filter]

# -------------------------
# Visualization 1: Histogram of Gift Amounts
# -------------------------
st.subheader("Distribution of Gift Amounts")

hist = (
    alt.Chart(df_filtered)
    .mark_bar()
    .encode(
        x=alt.X("Gift Amount:Q", bin=alt.Bin(maxbins=40)),
        y="count()",
        tooltip=["count()"]
    )
    .properties(width=600, height=300)
)

st.altair_chart(hist, use_container_width=True)

# -------------------------
# Visualization 2 + 3: Your Linked View
# -------------------------
st.subheader("Allocation Subcategory → College Linked View")

# ---- INSERT YOUR FINAL CODE HERE ----
subcategory_select = alt.selection_point(fields=['Allocation Subcategory'])

subcategory_chart = (
    alt.Chart(df_filtered)
    .mark_bar()
    .encode(
        y=alt.Y('Allocation Subcategory:N', sort='-x', title='Allocation Subcategory'),
        x=alt.X('sum(Gift Amount):Q', title='Total Gift Amount'),
        color=alt.condition(
            subcategory_select,
            alt.Color('Allocation Subcategory:N', legend=None),
            alt.value('lightgray')
        ),
        tooltip=[
            alt.Tooltip('Allocation Subcategory:N'),
            alt.Tooltip('sum(Gift Amount):Q', title='Total Gifts')
        ]
    )
    .add_params(subcategory_select)
    .properties(width=600, height=300)
)

college_chart = (
    alt.Chart(df_filtered)
    .mark_bar()
    .encode(
        y=alt.Y('College:N', sort='-x', title='College'),
        x=alt.X('sum(Gift Amount):Q', title='Total Gift Amount'),
        color=alt.Color('College:N', legend=None),
        tooltip=[
            alt.Tooltip('College:N'),
            alt.Tooltip('sum(Gift Amount):Q', title='Total Gifts')
        ]
    )
    .transform_filter(subcategory_select)
    .properties(width=600, height=300)
)

linked_view = alt.vconcat(subcategory_chart, college_chart).resolve_scale(color='independent')

st.altair_chart(linked_view, use_container_width=True)




