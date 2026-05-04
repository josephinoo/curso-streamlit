"""
2_Ventas.py — Analisis detallado de ventas por categoria y region.
"""

import streamlit as st
from utils import (
    sidebar_con_filtros,
    grafico_categoria_barras,
    grafico_margen_categoria,
    grafico_region_pie,
    grafico_region_barras,
    grafico_scatter_ventas_profit,
    grafico_categoria_treemap,
)

st.set_page_config(page_title="Ventas | RetailDash", layout="wide", initial_sidebar_state="collapsed")

df = sidebar_con_filtros()

st.title("Analisis de Ventas")
st.caption("Desglosa el rendimiento por categoria, region y la relacion ventas-ganancia.")
st.divider()

# ── Por categoría ─────────────────────────────────────────────────────────────
st.subheader("Por Categoria")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grafico_categoria_barras(df), use_container_width=True)
with col2:
    st.plotly_chart(grafico_margen_categoria(df), use_container_width=True)

st.divider()

# ── Por región ────────────────────────────────────────────────────────────────
st.subheader("Por Region")

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(grafico_region_pie(df), use_container_width=True)
with col4:
    st.plotly_chart(grafico_region_barras(df), use_container_width=True)

st.divider()

# ── Composición Treemap ────────────────────────────────────────────────────────
st.subheader("Composicion Categoria → Region")
st.plotly_chart(grafico_categoria_treemap(df), use_container_width=True)

st.divider()

# ── Scatter ventas vs ganancia ─────────────────────────────────────────────────
st.subheader("Relacion Ventas vs Ganancia")
st.info("Cada punto es una transaccion. El tamaño indica la cantidad de unidades vendidas.")
st.plotly_chart(grafico_scatter_ventas_profit(df), use_container_width=True)
