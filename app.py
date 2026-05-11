import streamlit as st
import pandas as pd
import pdfplumber
import plotly.express as px
import re

st.set_page_config(layout="wide")

st.title("NHM State Dashboard")

uploaded_file = st.file_uploader("Upload NHM PDF", type=["pdf"])

# -----------------------------
# EXTRACT TEXT FROM PDF
# -----------------------------
def extract_kpis(text):

    kpis = {}

    # Clean text
    clean_text = text.replace("\n", " ")

    patterns = {
        "Total Population": r"Total Population.*?([\d]+\.[\d]+)",
        "Urban Population": r"Urban Population.*?([\d]+\.[\d]+)",
        "Cities Covered": r"Cities covered.*?(\d+)",
        "Slum Population": r"Slum.*?population.*?([\d]+\.[\d]+)"
    }

    for key, pattern in patterns.items():

        match = re.search(pattern, clean_text, re.IGNORECASE)

        if match:
            kpis[key] = match.group(1)
        else:
            kpis[key] = "Not Found"

    return kpis

    full_text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                full_text += text + "\n"

    return full_text


# -----------------------------
# EXTRACT KPI VALUES
# -----------------------------
def extract_kpis(text):

    kpis = {}

    patterns = {
        "Total Population": r"Total Population.*?:\s*([\d\.]+)",
        "Urban Population": r"Urban Population.*?:\s*([\d\.]+)",
        "Cities Covered": r"Total Cities.*?:\s*(\d+)",
        "Slum Population": r"Slum.*population.*?:\s*([\d\.]+)"
    }

    for key, pattern in patterns.items():

        match = re.search(pattern, text)

        if match:
            kpis[key] = match.group(1)
        else:
            kpis[key] = "N/A"

    return kpis


# -----------------------------
# MAIN APP
# -----------------------------
if uploaded_file:

    text = extract_text_from_pdf(uploaded_file)

    # Extract KPIs
    kpis = extract_kpis(text)
states = [

    "Bihar",

    "Chhattisgarh",

    "Gujarat",

    "Jharkhand",

    "Madhya Pradesh",

    "Odisha",

    "Rajasthan",

    "Uttar Pradesh",

    "Uttarakhand"

]

selected_state = st.selectbox(

    "Select State",

    states

)

st.title(f"{selected_state} Health Dashboard")
st.header("State Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Population", kpis["Total Population"])
col2.metric("Urban Population", kpis["Urban Population"])
col3.metric("Cities Covered", kpis["Cities Covered"])
col4.metric("Slum Population", kpis["Slum Population"])

st.divider()

# -----------------------------
# SAMPLE DASHBOARD DATA
# -----------------------------
sample_df = pd.DataFrame({
        "Category": [
            "UPHC-AAM",
            "UCHC",
            "Polyclinic",
            "U-AAM"
        ],
        "Required": [702, 70, 117, 1755],
        "Functional": [445, 41, 307, 646]
    })

    # -----------------------------
    # CHARTS
    # -----------------------------
st.subheader("Health Infrastructure")

fig = px.bar(
        sample_df,
        x="Category",
        y=["Required", "Functional"],
        barmode="group",
        height=500
    )

st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # TABLE
    # -----------------------------
st.subheader("Infrastructure Table")

st.dataframe(sample_df, use_container_width=True)

st.divider()

    # -----------------------------
    # SERVICE DELIVERY
    # -----------------------------
st.subheader("Service Delivery")

service_df = pd.DataFrame({
        "Service": [
            "Eye Care",
            "ENT Care",
            "Mental Health",
            "Emergency Care"
        ],
        "Coverage": [58, 73, 73, 73]
    })

    fig2 = px.bar(
        service_df,
        x="Coverage",
        y="Service",
        orientation="h",
        height=400
    )

st.plotly_chart(fig2, use_container_width=True)

st.success("Dashboard generated successfully")
