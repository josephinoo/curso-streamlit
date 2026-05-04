"""
1_Resumen.py — Pagina de resumen ejecutivo: KPIs + tendencias temporales.
"""

import streamlit as st
from utils import sidebar_con_filtros, mostrar_kpis, grafico_ventas_tiempo, grafico_profit_tiempo, grafico_ventas_anuales

st.set_page_config(page_title="Resumen | RetailDash", layout="wide", initial_sidebar_state="collapsed")

df = sidebar_con_filtros()

st.title("Resumen Ejecutivo")
st.caption(f"Bienvenido/a, **{st.session_state.nombre}** · Rol: {st.session_state.rol}")
st.divider()

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.subheader("Indicadores Clave de Rendimiento")
mostrar_kpis(df)

st.divider()

# ── Tendencias ────────────────────────────────────────────────────────────────
st.subheader("Tendencias Temporales")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grafico_ventas_tiempo(df), use_container_width=True)
with col2:
    st.plotly_chart(grafico_profit_tiempo(df), use_container_width=True)

st.plotly_chart(grafico_ventas_anuales(df), use_container_width=True)

st.caption("Usa los filtros de la barra lateral para segmentar los datos.")
