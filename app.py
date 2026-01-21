import streamlit as st
import psycopg
import pandas as pd
import json
import io
from datetime import datetime, timedelta

from auth import verify_user, hash_pwd
from insert_log import insert_log
from fetch_logs import hamta_loggar
from db_config import DB_CONFIG


st.set_page_config(page_title="Logg Dashboard", layout="wide")


# ─────────────────────────────
# Val: Logga in / Registrera
# ─────────────────────────────
mode = st.radio("Välj", ["Logga in", "Registrera"], horizontal=True)


# ─────────────────────────────
# Registrering
# ─────────────────────────────
if mode == "Registrera":
    st.subheader("Skapa konto")

    new_user = st.text_input("Användarnamn")
    new_pwd = st.text_input("Lösenord", type="password")

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
                st.success("Konto skapat! Logga in.")
            except psycopg.errors.UniqueViolation:
                st.error("Användarnamnet finns redan.")
        else:
            st.warning("Fyll i alla fält.")

    st.stop()


# ─────────────────────────────
# Inloggning
# ─────────────────────────────
if "user_id" not in st.session_state:
    st.title("Logga in")

    username = st.text_input("Användarnamn")
    password = st.text_input("Lösenord", type="password")

    if st.button("Logga in"):
        result = verify_user(username, password)
        if result:
            user_id, role = result
            st.session_state.user = username
            st.session_state.user_id = user_id
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Fel användarnamn eller lösenord.")

    st.stop()


# ─────────────────────────────
# Dashboard
# ─────────────────────────────
st.sidebar.write(
    f"Användare: {st.session_state.user} ({st.session_state.role})"
)

st.title("Min loggöversikt")


# ─────────────────────────────
# Uppdatera sidan
# ─────────────────────────────
if st.button("🔄 Uppdatera"):
    st.rerun()


# ─────────────────────────────
# Ny logg
# ─────────────────────────────
with st.form("ny_logg"):
    level = st.selectbox("Nivå", ["INFO", "WARNING", "ERROR"])
    service = st.text_input("Tjänst")
    message = st.text_area("Meddelande")
    context_str = st.text_area("Context (JSON)", "{}")

    submitted = st.form_submit_button("Spara logg")
    if submitted:
        try:
            ctx = json.loads(context_str)
        except json.JSONDecodeError:
            ctx = {}

        insert_log(
            level,
            service,
            message,
            ctx,
            st.session_state.user_id,
        )
        st.success("Logg sparad!")


# ─────────────────────────────
# Visa loggar
# ─────────────────────────────
antal = st.slider("Antal rader", 10, 500, 50)

df = hamta_loggar(
    user_id=st.session_state.user_id,
    role=st.session_state.role,
    sida=1,
    antal_per_sida=antal,
)

if df.empty:
    st.info("Inga loggar hittades.")
else:
    st.dataframe(df, use_container_width=True)
# ─────────────────────────────
# Tidslinje – senaste 24h
# ─────────────────────────────
st.subheader("Tidslinje (senaste 24h)")

df["timestamp"] = pd.to_datetime(df["timestamp"])

last_24h = df[
    df["timestamp"] >= pd.Timestamp.now() - pd.Timedelta(hours=24)
]

if not last_24h.empty:
    timeline = (
        last_24h
        .groupby([last_24h["timestamp"].dt.floor("H"), "level"])
        .size()
        .unstack(fill_value=0)
    )
    st.line_chart(timeline)
else:
    st.info("Inga loggar de senaste 24 timmarna.")

# ─────────────────────────────
# Exportera till Excel
# ─────────────────────────────
if st.button("📥 Ladda ner Excel"):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Logs", index=False)

    buffer.seek(0)
    st.download_button(
        "📥 Ladda ner Excel-fil",
        data=buffer,
        file_name=f"logs_{datetime.now():%Y%m%d_%H%M}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )



st.subheader("Sammanfattning")
st.bar_chart(df["level"].value_counts())


# ─────────────────────────────
# Admin: rensa loggar
# ─────────────────────────────
if st.session_state.role == "admin":
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


# ─────────────────────────────
# Logga ut
# ─────────────────────────────
if st.sidebar.button("🚪 Logga ut"):
    st.session_state.clear()
    st.rerun()
