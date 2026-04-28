"""
MÓDULO 4 — BLOQUE 1
Ejercicio 1: El Problema de los Re-runs
========================================
OBJETIVO: Ver en vivo cuántas veces se re-ejecuta el script
cuando NO usamos st.form.

INSTRUCCIONES PARA EL PROFESOR:
1. Correr: streamlit run 01_problema_reruns.py
2. Pedirle al estudiante que mueva el slider o cambie la ciudad
3. Observar cómo el contador de re-ejecuciones sube con cada acción
4. Discutir: ¿Qué pasaría si cada re-run consultara una base de datos?
"""

import streamlit as st
import time

st.set_page_config(page_title="El Problema de los Re-runs", page_icon="⚠️")

# ── Contador de re-ejecuciones ────────────────────────────
if "runs" not in st.session_state:
    st.session_state.runs = 0

st.session_state.runs += 1

# ── Header ────────────────────────────────────────────────
st.title("⚠️ Problema: Re-ejecuciones Explosivas")
st.caption("Módulo 4 · Bloque 1 · Ejercicio 1")

# ── Mostrar contador de forma visible ─────────────────────
col_counter, col_warn = st.columns([1, 2])

with col_counter:
    st.metric(
        label="Re-ejecuciones del script",
        value=st.session_state.runs,
        delta="+1 ahora mismo"
    )

with col_warn:
    if st.session_state.runs < 3:
        st.info("👆 Mueve cualquier widget para ver el contador subir")
    elif st.session_state.runs < 8:
        st.warning(f"⚠️ Ya van {st.session_state.runs} re-ejecuciones...")
    else:
        st.error(f"💥 ¡{st.session_state.runs} re-ejecuciones! La DB estaría sufriendo")

st.divider()

# ── Simulación de consulta "costosa" ─────────────────────
st.subheader("Buscador SIN st.form")
st.caption("Cada widget que toques = 1 re-ejecución completa = 1 consulta a la DB")

# Simular que cada rerun "cuesta" tiempo
with st.spinner(f"🔄 Re-ejecutando script... (run #{st.session_state.runs})"):
    time.sleep(0.3)  # Simula consulta a DB

ciudad = st.selectbox(
    "Ciudad",
    ["Quito", "Guayaquil", "Cuenca"],
    help="Cambiar esto = 1 re-ejecución"
)  # ← rerun #1 por cambio

presupuesto = st.slider(
    "Presupuesto máximo ($)",
    50_000, 300_000, 100_000, step=5_000,
    help="Mover esto = 1 re-ejecución"
)  # ← rerun #2 por cambio

habitaciones = st.number_input(
    "Habitaciones mínimas",
    min_value=1, max_value=10, value=2,
    help="Cambiar esto = 1 re-ejecución"
)  # ← rerun #3 por cambio

tipo = st.selectbox(
    "Tipo de propiedad",
    ["Casa", "Departamento", "Oficina", "Local"],
    help="Cambiar esto = 1 re-ejecución"
)  # ← rerun #4 por cambio

# ── Resultado (se recalcula en CADA re-run) ───────────────
st.divider()
st.subheader("Resultado")
st.success(
    f"Buscando: {tipo} en {ciudad} · "
    f"≤ ${presupuesto:,} · {habitaciones}+ hab."
)

# ── Mensaje educativo ─────────────────────────────────────
st.divider()
with st.expander("📚 ¿Por qué es un problema?"):
    st.markdown("""
    **Cada vez que tocas un widget, Streamlit:**
    1. Para la ejecución actual
    2. Vuelve a ejecutar **todo el script** de arriba a abajo
    3. En este ejemplo, eso incluye el `time.sleep(0.3)` que simula una consulta a DB

    **Con 10 filtros reales:**
    - 10 re-ejecuciones por sesión de búsqueda
    - Cada una hace una consulta SQL
    - Con 50 usuarios → **500 consultas innecesarias por minuto**

    **La solución: `st.form` → ¡siguiente ejercicio!**
    """)

if st.button("🔄 Reiniciar contador"):
    st.session_state.runs = 0
    st.rerun()
