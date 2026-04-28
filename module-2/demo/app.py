# app.py — portada
import streamlit as st

# ⚠️ DEBE ser el PRIMER comando de Streamlit en el archivo
st.set_page_config(
    page_title="Dashboard Aranceles",
    page_icon="🇺🇸",
    layout="wide"
)

st.title("🇺🇸 Dashboard — Aranceles USA")
st.write("Bienvenido. Usa el menú lateral para navegar.")
st.info("👈 Selecciona una página en el menú de la izquierda")