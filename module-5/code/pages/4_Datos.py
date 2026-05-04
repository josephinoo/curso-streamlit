"""
4_Datos.py — Pagina de explorador de datos: tabla interactiva + descarga CSV.
"""

import streamlit as st
import pandas as pd
from utils import sidebar_con_filtros, fmt_money, calcular_kpis

st.set_page_config(page_title="Datos | RetailDash", layout="wide", initial_sidebar_state="collapsed")

df = sidebar_con_filtros()

st.title("Explorador de Datos")
st.caption("Inspecciona el dataset filtrado, ordena columnas y descarga el resultado.")
st.divider()

# ── Conteo rapido ─────────────────────────────────────────────────────────────
kpis = calcular_kpis(df)

c1, c2, c3 = st.columns(3)
c1.metric("Total de registros", f"{kpis['registros']:,}")
c2.metric("Ventas en el periodo", fmt_money(kpis["ventas"]))
c3.metric("Categorias distintas", df["Category"].nunique())

st.divider()

# ── Buscador y ordenamiento ───────────────────────────────────────────────────
st.subheader("Tabla de Datos")

col_buscar, col_orden, col_dir = st.columns([2, 1, 1])

with col_buscar:
    busqueda = st.text_input("Buscar en Categoria o Region", placeholder="Ej: Electronics, North...")
with col_orden:
    columna_orden = st.selectbox("Ordenar por", ["Date", "Sales", "Profit", "Quantity"])
with col_dir:
    direccion = st.radio("Direccion", ["Descendente", "Ascendente"], horizontal=True)

# Aplicar búsqueda
df_vista = df.copy()
if busqueda:
    mask = (
        df_vista["Category"].str.contains(busqueda, case=False, na=False) |
        df_vista["Region"].str.contains(busqueda, case=False, na=False)
    )
    df_vista = df_vista[mask]

# Aplicar orden
df_vista = df_vista.sort_values(columna_orden, ascending=(direccion == "Ascendente"))

st.caption(f"Mostrando {min(500, len(df_vista)):,} de {len(df_vista):,} registros.")

st.dataframe(
    df_vista.head(500).style.format({
        "Sales":          "${:,.2f}",
        "Profit":         "${:,.2f}",
        "Profit_Margin":  "{:.1f}%",
    }),
    use_container_width=True,
    height=420,
)

st.divider()

# ── Descarga ──────────────────────────────────────────────────────────────────
st.subheader("Descargar Datos")

col_dl1, col_dl2 = st.columns(2)

with col_dl1:
    csv = df_vista.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar CSV filtrado",
        data=csv,
        file_name="retaildash_datos_filtrados.csv",
        mime="text/csv",
        use_container_width=True,
    )

with col_dl2:
    resumen_cat = (
        df.groupby("Category")
        .agg(Ventas=("Sales", "sum"), Ganancia=("Profit", "sum"), Unidades=("Quantity", "sum"))
        .reset_index()
    )
    csv_resumen = resumen_cat.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar resumen por categoria",
        data=csv_resumen,
        file_name="retaildash_resumen_categoria.csv",
        mime="text/csv",
        use_container_width=True,
    )
