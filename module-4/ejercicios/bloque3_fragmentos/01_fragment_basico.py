"""
MÓDULO 4 — BLOQUE 3
Ejercicio 1: @st.fragment — Re-ejecución Parcial
=================================================
OBJETIVO: Ver en vivo que una sección de la app se re-ejecuta
sin afectar al resto cuando se usa @st.fragment.

INSTRUCCIONES PARA EL PROFESOR:
1. Correr: streamlit run 01_fragment_basico.py
2. Hacer clic en los botones del panel de acciones
3. Observar que el SPINNER no vuelve a aparecer
4. Observar que el contador de re-runs del fragmento sube
   pero el de la app principal NO
"""

import streamlit as st
import time
import random

st.set_page_config(page_title="@st.fragment Básico", page_icon="⚡")

st.title("⚡ @st.fragment — Re-ejecución Parcial")
st.caption("Módulo 4 · Bloque 3 · Ejercicio 1")

# ── Contadores ────────────────────────────────────────────
if "app_runs" not in st.session_state:
    st.session_state.app_runs = 0
if "frag_runs" not in st.session_state:
    st.session_state.frag_runs = 0
if "favorito" not in st.session_state:
    st.session_state.favorito = False

st.session_state.app_runs += 1

# ── Contadores visibles ───────────────────────────────────
col_a, col_b = st.columns(2)
col_a.metric(
    "Re-ejecuciones de la APP COMPLETA",
    st.session_state.app_runs,
    help="Sube solo cuando algo fuera del fragmento cambia"
)
col_b.metric(
    "Re-ejecuciones del FRAGMENTO",
    st.session_state.frag_runs,
    help="Sube cuando interactúas DENTRO del fragmento"
)
st.divider()

# ─────────────────────────────────────────────────────────
# SECCIÓN PESADA — solo se ejecuta al inicio o al recargar
# ─────────────────────────────────────────────────────────
st.subheader("📊 Análisis Inmobiliario (sección pesada)")

with st.spinner("⏳ Cargando análisis... (simula 2s de DB)"):
    time.sleep(2)  # Esta línea NO corre cuando interactúas con el fragmento

import pandas as pd, numpy as np
np.random.seed(42)
df_chart = pd.DataFrame({
    "mes":    ["Ene","Feb","Mar","Abr","May","Jun"],
    "precio": [120, 135, 118, 145, 138, 152],
    "ventas": [23, 31, 19, 28, 35, 42],
})
st.line_chart(df_chart.set_index("mes"), use_container_width=True)
st.caption("✅ Si interactúas con los botones de abajo, este gráfico NO parpadea")

st.divider()

# ─────────────────────────────────────────────────────────
# FRAGMENTO — re-ejecuta solo esta función cuando el usuario
# interactúa desde adentro
# ─────────────────────────────────────────────────────────
@st.fragment
def panel_acciones():
    """Este bloque tiene su propio ciclo de vida."""
    st.session_state.frag_runs += 1

    st.subheader("⚡ Panel de Acciones (fragmento)")
    st.caption("Los botones de aquí NO recargan el gráfico de arriba")

    col1, col2, col3 = st.columns(3)

    # Toggle favorito
    fav = col1.toggle("⭐ Favorito", value=st.session_state.favorito)
    if fav != st.session_state.favorito:
        st.session_state.favorito = fav

    # Botón compartir
    if col2.button("📤 Compartir"):
        st.toast("¡Enlace copiado al portapapeles!", icon="📤")

    # Botón actualizar precio
    if col3.button("🔄 Actualizar precio"):
        nuevo_precio = random.randint(140_000, 200_000)
        st.toast(f"Precio actualizado: ${nuevo_precio:,}", icon="💰")

    # Estado visual
    if st.session_state.favorito:
        st.success("⭐ Esta propiedad está en tus favoritos")
    else:
        st.info("Haz clic en ⭐ Favorito para guardarlo")

    # Notas del usuario
    nota = st.text_area(
        "📝 Notas personales",
        placeholder="Escribe notas sobre esta propiedad...",
        height=80
    )
    if nota:
        st.caption(f"💾 Auto-guardando: {nota[:30]}...")

# Llamar al fragmento — desde aquí en adelante tiene ciclo propio
panel_acciones()

# ─────────────────────────────────────────────────────────
st.divider()
with st.expander("📚 ¿Cómo funciona @st.fragment?"):
    st.code("""
# Sin @st.fragment:
# Al hacer clic en un botón → TODO el script corre de nuevo
# El gráfico se recarga, el spinner aparece, tarda 2 segundos

# Con @st.fragment:
# Al hacer clic en un botón DENTRO del fragmento →
# SOLO esa función se re-ejecuta
# El gráfico de arriba queda INTACTO

@st.fragment
def mi_fragmento():
    if st.button("Clic rápido"):
        st.balloons()   # Solo esto corre al hacer clic
    """, language="python")
    st.markdown("""
    **Reglas de @st.fragment:**
    - El fragmento NO puede acceder a widgets definidos fuera de él
    - Puede leer y escribir `st.session_state`
    - `st.rerun()` dentro del fragmento solo re-ejecuta el fragmento
    - Para re-ejecutar toda la app: `st.rerun(scope='app')`
    """)
