import streamlit as st
import pandas as pd

st.title("📊 Tabla de Aranceles")
archivo = st.sidebar.file_uploader("Sube el CSV", type=["csv"])

if archivo is None:
    st.info("Sube el archivo CSV desde el panel lateral.")
    st.stop()

df = pd.read_csv(archivo)
col1, col2, col3 = st.columns(3)
col1.metric("Filas",   len(df),border=True)
col2.metric("Países",  df["country"].nunique(),border=True)
col3.metric("Máx %", f"{df['tariff_rate_pct'].max():.1f}%",border=True)
