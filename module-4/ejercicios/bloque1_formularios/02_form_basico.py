"""
MÓDULO 4 — BLOQUE 1
Ejercicio 2: st.form — La Solución
====================================
OBJETIVO: Ver la diferencia entre tener widgets dentro y
fuera de un st.form. Comparar el contador de reruns.

INSTRUCCIONES PARA EL PROFESOR:
1. Correr: streamlit run 02_form_basico.py
2. Mostrar que mover los sliders NO incrementa el contador
3. Presionar el botón → solo entonces sube el contador
4. Comparar con el ejercicio 01
"""

import streamlit as st
import time
import pandas as pd
import numpy as np

st.set_page_config(page_title="st.form — La Solución", page_icon="📋")

# ── Contador de re-ejecuciones ────────────────────────────
if "runs" not in st.session_state:
    st.session_state.runs = 0
if "busquedas" not in st.session_state:
    st.session_state.busquedas = 0

st.session_state.runs += 1

# ── Header ────────────────────────────────────────────────
st.title("📋 st.form — El Carrito de Compras")
st.caption("Módulo 4 · Bloque 1 · Ejercicio 2")

# ── Contador visible ──────────────────────────────────────
col1, col2 = st.columns(2)
col1.metric("Re-ejecuciones del script", st.session_state.runs)
col2.metric("Búsquedas realizadas", st.session_state.busquedas)

st.caption(
    "👆 Mueve los sliders — el contador de re-ejecuciones NO sube. "
    "Solo sube cuando presionas el botón."
)
st.divider()

# ── Generar datos de ejemplo ──────────────────────────────
@st.cache_data
def generar_propiedades() -> pd.DataFrame:
    """Genera un DataFrame de ejemplo — carga UNA sola vez."""
    np.random.seed(42)
    n = 200
    ciudades = ["Quito", "Guayaquil", "Cuenca"]
    tipos    = ["Casa", "Departamento", "Oficina"]
    return pd.DataFrame({
        "id":           range(1, n + 1),
        "ciudad":       np.random.choice(ciudades, n),
        "tipo":         np.random.choice(tipos, n),
        "precio":       np.random.randint(50_000, 400_000, n),
        "habitaciones": np.random.randint(1, 6, n),
        "area_m2":      np.random.randint(40, 300, n),
        "nueva":        np.random.choice([True, False], n),
    })

df = generar_propiedades()

# ── Formulario de búsqueda ────────────────────────────────
st.subheader("🔍 Buscador con st.form")

with st.form("buscador_propiedades"):
    st.write("**Configura todos tus filtros y presiona Buscar al final:**")

    col_a, col_b = st.columns(2)

    ciudad = col_a.selectbox(
        "Ciudad",
        ["Todas"] + sorted(df["ciudad"].unique().tolist())
    )
    tipo = col_b.selectbox(
        "Tipo de propiedad",
        ["Todos"] + sorted(df["tipo"].unique().tolist())
    )

    presupuesto_max = st.slider(
        "Presupuesto máximo ($)",
        min_value=50_000,
        max_value=400_000,
        value=200_000,
        step=10_000,
        format="$%d"
    )

    col_c, col_d = st.columns(2)
    min_hab  = col_c.number_input("Habitaciones mínimas", 1, 5, 1)
    solo_new = col_d.checkbox("Solo propiedades nuevas")

    # El único botón que dispara el rerun
    col_btn1, col_btn2 = st.columns([1, 3])
    buscar  = col_btn1.form_submit_button("🔍 Buscar", type="primary")
    limpiar = col_btn2.form_submit_button("🗑️ Limpiar filtros")

# ── Procesar búsqueda ─────────────────────────────────────
if buscar:
    st.session_state.busquedas += 1

    with st.spinner("Consultando base de datos..."):
        time.sleep(0.5)  # Simula consulta real

    # Aplicar filtros
    resultado = df.copy()
    if ciudad != "Todas":
        resultado = resultado[resultado["ciudad"] == ciudad]
    if tipo != "Todos":
        resultado = resultado[resultado["tipo"] == tipo]
    resultado = resultado[resultado["precio"] <= presupuesto_max]
    resultado = resultado[resultado["habitaciones"] >= min_hab]
    if solo_new:
        resultado = resultado[resultado["nueva"] == True]

    # Mostrar resultados
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Propiedades encontradas", len(resultado))
    m2.metric("Precio promedio", f"${resultado['precio'].mean():,.0f}" if len(resultado) else "-")
    m3.metric("Área promedio (m²)", f"{resultado['area_m2'].mean():.0f}" if len(resultado) else "-")

    if len(resultado) > 0:
        st.dataframe(
            resultado.sort_values("precio"),
            use_container_width=True,
            hide_index=True,
            column_config={
                "precio": st.column_config.NumberColumn("Precio ($)", format="$%d"),
                "area_m2": st.column_config.NumberColumn("Área (m²)", format="%d m²"),
                "nueva": st.column_config.CheckboxColumn("Nueva"),
            }
        )
    else:
        st.warning("No se encontraron propiedades con esos filtros.")

elif limpiar:
    st.info("Filtros limpiados. Configura nueva búsqueda.")

# ── Nota educativa ────────────────────────────────────────
st.divider()
with st.expander("📚 ¿Por qué funciona mejor?"):
    st.markdown("""
    **Dentro de `st.form`, ningún widget dispara re-ejecuciones.**

    El flujo es:
    1. El usuario configura **todos los filtros** tranquilamente
    2. Presiona **"Buscar"** una sola vez
    3. **Solo entonces** Streamlit re-ejecuta el script y consulta la DB

    **Reglas importantes:**
    - El `key` del form (`"buscador_propiedades"`) debe ser **único** en la app
    - `st.button` normal **NO funciona** dentro de un form — usa `st.form_submit_button`
    - Puedes tener **múltiples** `form_submit_button` con distintas acciones
    - Puedes usar `st.columns`, `st.tabs`, `st.divider` dentro del form
    """)
