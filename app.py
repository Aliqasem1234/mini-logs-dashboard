# app.py
import streamlit as st
from fetch_logs import hamta_loggar
from insert_log import insert_log
import pandas as pd
import json

st.set_page_config(page_title="Logg Dashboard", layout="wide")
st.title("Min loggöversikt")

# ── formulär för ny logg ----------
with st.form("ny_logg"):
    col1, col2 = st.columns(2)
    with col1:
        level = st.selectbox("Nivå", ["INFO", "WARNING", "ERROR"])
        service = st.text_input("Tjänst")
    with col2:
        message = st.text_area("Meddelande")
    context_str = st.text_area("Context (JSON, frivillig)", "{}")
    submitted = st.form_submit_button("Spara logg")
    if submitted:
        try:
            ctx = json.loads(context_str)
        except Exception:
            ctx = {}
        insert_log(level, service, message, ctx)
        st.success("Logg sparad!")

# ── visa tabell --------------------
antal = st.slider("Antal rader att visa", 10, 500, 50)
df = hamta_loggar(antal)
st.dataframe(df, use_container_width=True)

# ── sammanfattning -----------------
st.subheader("Sammanfattning")
st.bar_chart(df['level'].value_counts())