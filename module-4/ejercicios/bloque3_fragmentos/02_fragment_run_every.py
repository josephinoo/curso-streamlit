"""
MÓDULO 4 — BLOQUE 3
Ejercicio 2: run_every — Dashboard en Tiempo Real
==================================================
OBJETIVO: Usar @st.fragment(run_every=N) para que una sección
se actualice automáticamente sin que el usuario haga nada.

INSTRUCCIONES PARA EL PROFESOR:
1. Correr: streamlit run 02_fragment_run_every.py
2. No tocar nada — los KPIs cambian solos cada 3 segundos
3. Mover el slider de período — el gráfico histórico se recarga
   PERO los KPIs siguen actualizándose independientemente
4. Mostrar que run_every acepta segundos, strings ("5s", "1m"), o timedelta
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import time

st.set_page_config(
    page_title="Live Dashboard",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Dashboard en Tiempo Real — @st.fragment(run_every)")
st.caption("Módulo 4 · Bloque 3 · Ejercicio 2")

# ── Contadores ────────────────────────────────────────────
if "app_runs_live" not in st.session_state:
    st.session_state.app_runs_live = 0
if "kpi_updates" not in st.session_state:
    st.session_state.kpi_updates = 0

st.session_state.app_runs_live += 1

col_cnt1, col_cnt2, col_config = st.columns([1, 1, 2])
col_cnt1.metric("Re-runs de la app", st.session_state.app_runs_live)
col_cnt2.metric("Actualizaciones de KPIs", st.session_state.kpi_updates)
with col_config:
    intervalo = st.slider(
        "⏱️ Intervalo de actualización (segundos)",
        min_value=1, max_value=10, value=3,
        help="Cada cuántos segundos se actualizan los KPIs"
    )

st.divider()

# ─────────────────────────────────────────────────────────
# SECCIÓN PESADA — gráfico histórico
# ─────────────────────────────────────────────────────────
st.subheader("📊 Datos Históricos")

periodo = st.radio(
    "Período",
    ["7 días", "30 días", "90 días"],
    horizontal=True
)

@st.cache_data(show_spinner=False)
def cargar_historico(periodo_str: str) -> pd.DataFrame:
    """Simula carga de datos históricos — tarda un momento."""
    dias = int(periodo_str.split()[0])
    np.random.seed(hash(periodo_str) % 1000)
    fechas = pd.date_range(end=pd.Timestamp.today(), periods=dias, freq="D")
    return pd.DataFrame({
        "fecha":  fechas,
        "ventas": np.random.randint(5, 30, dias),
        "leads":  np.random.randint(15, 60, dias),
        "precio_prom": np.random.randint(100, 200, dias),
    })

with st.spinner(f"Cargando datos de {periodo}..."):
    df_hist = cargar_historico(periodo)
    time.sleep(0.5)

st.line_chart(
    df_hist.set_index("fecha")[["ventas", "leads"]],
    use_container_width=True,
    color=["#FF4B4B", "#3b82f6"]
)
st.caption(f"📊 {len(df_hist)} días de datos · Cambia el período para recargar")

st.divider()

# ─────────────────────────────────────────────────────────
# FRAGMENTO CON run_every — se actualiza automáticamente
# ─────────────────────────────────────────────────────────

@st.fragment(run_every=intervalo)
def kpis_en_vivo():
    """
    Este fragmento se re-ejecuta cada {intervalo} segundos.
    El gráfico histórico de arriba NO se recarga.
    """
    st.session_state.kpi_updates += 1

    # Simular datos en tiempo real desde una API
    ts = time.strftime("%H:%M:%S")
    ventas_hoy  = random.randint(80, 180)
    ticket_prom = random.uniform(45.0, 120.0)
    activos     = random.randint(8, 45)
    conversión  = random.uniform(2.0, 9.0)

    st.subheader("⚡ KPIs en Tiempo Real")
    st.caption(f"Auto-actualización cada {intervalo}s · Última: {ts}")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "💰 Ventas hoy",
        f"${ventas_hoy:,}k",
        delta=f"{random.choice(['+', '-'])}{random.randint(1, 15)}%"
    )
    m2.metric(
        "🎫 Ticket promedio",
        f"${ticket_prom:.0f}",
        delta=f"{random.choice(['+', '-'])}{random.uniform(1, 8):.1f}%"
    )
    m3.metric(
        "👥 Usuarios activos",
        activos,
        delta=random.randint(-5, 8)
    )
    m4.metric(
        "📈 Tasa conversión",
        f"{conversión:.1f}%",
        delta=f"{random.choice(['+', '-'])}{random.uniform(0.1, 1.5):.1f}%"
    )

    # Mini gráfico de barras en tiempo real
    df_live = pd.DataFrame({
        "hora":   [f"{h}:00" for h in range(9, 19)],
        "ventas": [random.randint(2, 20) for _ in range(10)],
    })
    st.bar_chart(df_live.set_index("hora"), height=150, use_container_width=True)

kpis_en_vivo()

# ─────────────────────────────────────────────────────────
st.divider()
with st.expander("📚 Cómo usar run_every"):
    st.code("""
# Opciones para run_every:
@st.fragment(run_every=5)           # cada 5 segundos
@st.fragment(run_every="10s")       # cada 10 segundos
@st.fragment(run_every="1m")        # cada 1 minuto
@st.fragment(run_every="2h")        # cada 2 horas

from datetime import timedelta
@st.fragment(run_every=timedelta(seconds=30))  # con timedelta

# El fragmento se actualiza AUTOMÁTICAMENTE
# incluso si el usuario no hace nada
    """, language="python")
    st.markdown("""
    **Casos de uso ideales para `run_every`:**
    - KPIs de ventas en tiempo real
    - Estado de pedidos o inventario
    - Métricas de un servidor o API
    - Precios de activos financieros
    - Estado de procesos en background
    """)
