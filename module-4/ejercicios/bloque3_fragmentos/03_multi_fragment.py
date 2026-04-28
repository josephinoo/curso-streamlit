"""
MÓDULO 4 — BLOQUE 3
Ejercicio 3: Múltiples Fragmentos Independientes
=================================================
OBJETIVO: Mostrar cómo varios fragmentos coexisten en la misma
app con ciclos de vida completamente independientes.

INSTRUCCIONES PARA EL PROFESOR:
1. Correr: streamlit run 03_multi_fragment.py
2. Interactuar con el panel de favoritos → solo ese fragmento corre
3. Escribir en el chat → solo el fragmento del chat corre
4. Los KPIs se actualizan solos cada 5s
5. Cambiar el selectbox de sección → solo eso recarga la app
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import time

st.set_page_config(
    page_title="Multi-Fragment",
    page_icon="🧩",
    layout="wide"
)

st.title("🧩 Múltiples Fragmentos Independientes")
st.caption("Módulo 4 · Bloque 3 · Ejercicio 3")

# ── Estado global ─────────────────────────────────────────
if "favoritos" not in st.session_state:
    st.session_state.favoritos = []
if "chat_msgs" not in st.session_state:
    st.session_state.chat_msgs = [
        {"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte con tu búsqueda?"}
    ]
if "app_runs_m" not in st.session_state:
    st.session_state.app_runs_m = 0
if "fav_runs" not in st.session_state:
    st.session_state.fav_runs = 0
if "chat_runs" not in st.session_state:
    st.session_state.chat_runs = 0
if "kpi_runs_m" not in st.session_state:
    st.session_state.kpi_runs_m = 0

st.session_state.app_runs_m += 1

# ── Contador de runs ──────────────────────────────────────
with st.expander("🔢 Contador de re-ejecuciones por sección"):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("App completa", st.session_state.app_runs_m)
    c2.metric("Panel favoritos", st.session_state.fav_runs)
    c3.metric("Chat", st.session_state.chat_runs)
    c4.metric("KPIs live", st.session_state.kpi_runs_m)

st.divider()

# ── Selectbox FUERA de fragmentos ─────────────────────────
seccion = st.selectbox(
    "📂 Sección a ver",
    ["🏠 Propiedades disponibles", "📈 Tendencias del mercado", "🗺️ Mapa de zonas"],
    help="Cambiar esto recarga la app completa, pero los fragmentos se mantienen"
)

# ── Contenido de la sección (cambia con el selectbox) ─────
@st.cache_data
def datos_propiedades():
    np.random.seed(7)
    return pd.DataFrame({
        "id":     range(1, 11),
        "nombre": [f"Propiedad #{i}" for i in range(1, 11)],
        "ciudad": np.random.choice(["Quito", "Guayaquil", "Cuenca"], 10),
        "precio": np.random.randint(80_000, 350_000, 10),
        "hab":    np.random.randint(1, 5, 10),
    })

df_props = datos_propiedades()

if "Propiedades" in seccion:
    st.dataframe(df_props, use_container_width=True, hide_index=True,
                 column_config={"precio": st.column_config.NumberColumn("Precio", format="$%d")})
elif "Tendencias" in seccion:
    np.random.seed(42)
    df_tend = pd.DataFrame({"mes": range(1, 13), "precio_prom": np.random.randint(100, 200, 12)})
    st.line_chart(df_tend.set_index("mes"), use_container_width=True)
else:
    st.info("🗺️ Aquí iría un mapa interactivo con folium o pydeck")

st.divider()

# ─────────────────────────────────────────────────────────
# Layout: dos columnas para los fragmentos
# ─────────────────────────────────────────────────────────
col_izq, col_der = st.columns([2, 1])

# ── FRAGMENTO 1: Panel de favoritos ───────────────────────
with col_izq:
    @st.fragment
    def panel_favoritos():
        st.session_state.fav_runs += 1
        st.subheader("⭐ Favoritos")

        opciones = [f"Propiedad #{i}" for i in range(1, 11)]
        seleccion = st.multiselect(
            "Agregar a favoritos",
            opciones,
            default=st.session_state.favoritos,
            key="fav_select"
        )
        st.session_state.favoritos = seleccion

        if seleccion:
            st.success(f"✅ {len(seleccion)} propiedad(es) en favoritos")
            for fav in seleccion:
                st.markdown(f"⭐ {fav}")
        else:
            st.info("Selecciona propiedades arriba para guardarlas")

        if st.button("🗑️ Limpiar favoritos", disabled=not seleccion):
            st.session_state.favoritos = []
            st.rerun(scope="fragment")

    panel_favoritos()

    # ── FRAGMENTO 2: KPIs en vivo ──────────────────────────
    st.divider()

    @st.fragment(run_every=5)
    def kpis_mini():
        st.session_state.kpi_runs_m += 1
        st.caption(f"⚡ KPIs · Auto-update cada 5s · {time.strftime('%H:%M:%S')}")
        m1, m2 = st.columns(2)
        m1.metric("Visitas hoy", random.randint(200, 600), random.randint(-20, 50))
        m2.metric("Consultas", random.randint(15, 45), random.randint(-5, 10))

    kpis_mini()

# ── FRAGMENTO 3: Chat ─────────────────────────────────────
with col_der:
    @st.fragment
    def mini_chat():
        st.session_state.chat_runs += 1
        st.subheader("💬 Asistente")

        # Mostrar mensajes
        chat_container = st.container(height=300)
        with chat_container:
            for msg in st.session_state.chat_msgs:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        # Input
        pregunta = st.chat_input("Pregunta algo...", key="chat_frag_input")
        if pregunta:
            st.session_state.chat_msgs.append({"role": "user", "content": pregunta})

            # Respuesta simple de demostración
            respuestas = [
                f"Encontré 5 opciones para '{pregunta[:20]}'...",
                "¡Excelente pregunta! Te puedo ayudar con eso.",
                f"Basándome en tu búsqueda: {pregunta[:15]}..., recomiendo Quito Norte.",
                "El precio promedio para eso es $145,000.",
            ]
            respuesta = random.choice(respuestas)
            st.session_state.chat_msgs.append({"role": "assistant", "content": respuesta})
            st.rerun(scope="fragment")

        if st.button("🗑️ Limpiar chat", key="clear_chat"):
            st.session_state.chat_msgs = [
                {"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte?"}
            ]
            st.rerun(scope="fragment")

    mini_chat()
