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
def clean_dataframe(df):
    df = df.fillna("")

    # Remove unwanted rows
    df = df[~df[0].str.contains("High Focus|NATIONAL|Status", na=False)]

    # Find header row
    header_index = df[df[0].str.contains("SL No", na=False)].index

    if len(header_index) > 0:
        header_row = header_index[0]
        df.columns = df.iloc[header_row]
        df = df[header_row + 1:]

    df = df.reset_index(drop=True)

    return df
    st.write("Raw Extracted Data Preview:")
    st.dataframe(df.head())

    st.warning("⚠️ This is a basic extraction. We will structure it next.")
