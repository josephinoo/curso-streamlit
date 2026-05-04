import pandas as pd
import numpy as np
import streamlit as st


# Coordenadas aproximadas por región (para el mapa)
REGION_COORDS = {
    "North":   {"lat": 43.0, "lon": -85.0},
    "South":   {"lat": 30.0, "lon": -90.0},
    "East":    {"lat": 40.7, "lon": -74.0},
    "West":    {"lat": 37.8, "lon": -120.5},
    "Central": {"lat": 41.8, "lon": -93.0},
}


@st.cache_data(show_spinner="Cargando y limpiando datos...")
def cargar_datos(ruta: str = "data/retail_sales.csv") -> pd.DataFrame:
    """
    Carga el CSV del dataset de Kaggle, aplica limpieza y devuelve un
    DataFrame listo para análisis.

    Pasos de limpieza:
    1. Parsear fechas
    2. Eliminar filas donde Category == 'NaN?' o es nulo
    3. Eliminar filas con Sales / Profit / Quantity nulos o negativos
    4. Resetear índice
    """
    try:
        df = pd.read_csv(ruta, parse_dates=["Date"])
    except FileNotFoundError:
        # ── Si no existe el CSV, generamos datos sintéticos para demo ────────
        st.warning("No se encontró 'retail_sales_dataset.csv'. Usando datos de demostración.")
        df = _generar_datos_demo()

    # ── Limpieza ──────────────────────────────────────────────────────────────
    # 1. Eliminar 'NaN?' y valores nulos en Category
    df = df[~df["Category"].astype(str).str.strip().isin(["NaN?", "nan", "NaN", ""])]
    df = df.dropna(subset=["Category"])

    # 2. Eliminar filas con valores críticos nulos
    df = df.dropna(subset=["Sales", "Profit", "Quantity", "Date", "Region"])

    # 3. Eliminar negativos en Sales y Quantity (datos anómalos)
    df = df[(df["Sales"] >= 0) & (df["Quantity"] >= 0)]

    # 4. Normalizar strings
    df["Category"] = df["Category"].str.strip().str.title()
    df["Region"]   = df["Region"].str.strip().str.title()

    # 5. Columnas derivadas útiles
    df["Month"]        = df["Date"].dt.to_period("M").astype(str)
    df["Year"]         = df["Date"].dt.year
    df["Profit_Margin"] = (df["Profit"] / df["Sales"].replace(0, np.nan)) * 100

    df = df.reset_index(drop=True)
    return df


def _generar_datos_demo() -> pd.DataFrame:
    """Genera un DataFrame sintético que imita el dataset de Kaggle."""
    np.random.seed(42)
    n = 1200

    categorias = ["Electronics", "Furniture", "Office Supplies", "Clothing", "Food & Beverages"]
    regiones   = ["North", "South", "East", "West", "Central"]
    fechas     = pd.date_range("2022-01-01", "2024-12-31", periods=n)

    cat = np.random.choice(categorias, n)
    reg = np.random.choice(regiones,   n)

    # Ventas con variación por categoría
    base_ventas = {"Electronics": 800, "Furniture": 600, "Office Supplies": 200,
                   "Clothing": 150, "Food & Beverages": 100}
    sales = np.array([base_ventas[c] * (1 + np.random.randn() * 0.4) for c in cat]).clip(10)

    quantity = np.random.randint(1, 50, n)
    profit   = sales * np.random.uniform(0.05, 0.35, n)

    return pd.DataFrame({
        "Date":     fechas,
        "Category": cat,
        "Sales":    sales.round(2),
        "Quantity": quantity,
        "Profit":   profit.round(2),
        "Region":   reg,
    })
