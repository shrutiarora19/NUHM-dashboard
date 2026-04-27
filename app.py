import streamlit as st
import pandas as pd
import plotly.express as px

st.title("NHM State Dashboard")

uploaded_file = st.file_uploader("Upload NHM PDF (converted to CSV for now)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    state = st.selectbox("Select State", df["State"].unique())

    state_df = df[df["State"] == state]

    st.subheader(f"{state} Dashboard")

    fig = px.bar(
        state_df.head(10),
        x="Value",
        y="Indicator",
        orientation="h"
    )

    st.plotly_chart(fig)
