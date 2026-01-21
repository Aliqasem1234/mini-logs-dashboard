import streamlit as st
from fetch_logs import hamta_loggar
from insert_log import insert_log
from auth import hash_pwd, verify_user
from db_config import DB_CONFIG

import psycopg
import pandas as pd
import json
import io
from datetime import datetime, timedelta


# ─────────────────────────────────────────────
# Sidkonfiguration (ska vara högst upp)
# ─────────────────────────────────────────────
st.set_page_config(page_title="Logg Dashboard", layout="wide")


# ─────────────────────────────────────────────
# Val av läge: Logga in eller Registrera
# ─────────────────────────────────────────────
mode = st.radio("Välj", ["Logga in", "Registrera"], horizontal=True)


# ─────────────────────────────────────────────
# Registreringsvy – skapa nytt konto
# ─────────────────────────────────────────────
if mode == "Registrera":
    st.subheader("Skapa konto")

    new_user = st.text_input("Användarnamn", key="reg_user")
    new_pwd = st.text_input("Lösenord", type="password", key="reg_pwd")

    if st.button("Registrera"):
        if new_user and new_pwd:
            try:
                with psycopg.connect(**DB_CONFIG) as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            INSERT INTO users (username, password_hash, role)
                            VALUES (%s, %s, 'viewer')
                            """,
                            (new_user, hash_pwd(new_pwd)),
                        )
                    conn.commit()
                st.success("Konto skapat! Logga in ovan.")
            except psycopg.errors.UniqueViolation:
                st.error("Användarnamnet finns redan.")
        else:
            st.warning("Fyll i alla fält.")

    st.stop()


# ─────────────────────────────────────────────
# Inloggningsvy (om ingen session finns)
# ─────────────────────────────────────────────
if "user" not in st.session_state:
    st.title("Logga in")

    username = st.text_input("Användarnamn")
    password = st.text_input("Lösenord", type="password")

    if st.button("Logga in"):
        role = verify_user(username, password)
        if role:
            st.session_state.user = username
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Fel användarnamn eller lösenord.")

    st.stop()


# ─────────────────────────────────────────────
# Användarinformation & sidhuvud
# ─────────────────────────────────────────────
role = st.session_state.role
st.sidebar.write(f"Användare: {st.session_state.user} ({role})")

st.title("Min loggöversikt")


# ─────────────────────────────────────────────
# Formulär för att skapa ny logg
# ─────────────────────────────────────────────
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
        except json.JSONDecodeError:
            ctx = {}

        insert_log(level, service, message, ctx)
        st.success("Logg sparad!")


# ─────────────────────────────────────────────
# Manuell uppdatering
# ─────────────────────────────────────────────
if st.button("🔄 Hämta igen"):
    st.rerun()


# ─────────────────────────────────────────────
# Hämtning och visning av loggar
# ─────────────────────────────────────────────
antal = st.slider("Antal rader att visa", 10, 500, 50)
df = hamta_loggar(sida=1, antal_per_sida=antal)

if df.empty:
    st.warning("Inga loggar hittades – lägg till en ny post.")
else:
    st.dataframe(df, use_container_width=True)

    # Sammanfattning per nivå
    st.subheader("Sammanfattning")
    order = ["INFO", "WARNING", "ERROR"]
    counts = df["level"].value_counts().reindex(order, fill_value=0)
    st.bar_chart(counts)

    # Tidslinje (senaste 24 timmarna)
    st.subheader("Tidslinje (senaste 24h)")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    last_24h = df[df["timestamp"] >= pd.Timestamp.now() - pd.Timedelta(hours=24)]

    timeline = (
        last_24h.groupby([last_24h["timestamp"].dt.floor("H"), "level"])
        .size()
        .unstack(fill_value=0)
    )

    st.line_chart(timeline)

    # Export till Excel
    if st.button("📥 Ladda ner Excel"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Logs", index=False)

        buffer.seek(0)
        st.download_button(
            "📥 Excel",
            data=buffer,
            file_name=f"logs_{datetime.now():%Y%m%d_%H%M}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


# ─────────────────────────────────────────────
# Admin-funktion: rensa gamla loggar
# ─────────────────────────────────────────────
if role == "admin":
    if st.button("🗑 Rensa loggar äldre än 30 dagar"):
        cutoff = datetime.utcnow() - timedelta(days=30)

        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM logs WHERE timestamp < %s",
                    (cutoff,),
                )
            conn.commit()

        st.success("Gamla loggar borttagna!")
        st.rerun()


# ─────────────────────────────────────────────
# Logga ut
# ─────────────────────────────────────────────
if st.sidebar.button("🚪 Logga ut"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
