import streamlit as st
import pandas as pd
import pdfplumber
import plotly.express as px

st.title("NHM State Dashboard")

uploaded_file = st.file_uploader("Upload NHM PDF", type=["pdf"])

def extract_table_from_pdf(file):
    all_rows = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    all_rows.append(row)

    df = pd.DataFrame(all_rows)

    # Basic cleaning (adjust if needed)
    df = df.dropna(how="all")
    df = df.reset_index(drop=True)

    return df

if uploaded_file:

    df = extract_table_from_pdf(uploaded_file)
    st.write("Raw Extracted Data Preview:")
    st.dataframe(df.head())

    st.warning("⚠️ This is a basic extraction. We will structure it next.")
