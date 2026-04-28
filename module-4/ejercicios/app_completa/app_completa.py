"""
MÓDULO 4 — APP COMPLETA
Plataforma Inmobiliaria IA — Integración de todos los bloques
=============================================================
OBJETIVO: App final que integra login, formulario, fragmentos y chat
en una sola aplicación profesional multi-página.

INSTRUCCIONES PARA EL PROFESOR:
1. Correr: streamlit run app_completa.py
2. Login con: ana / pass123  (admin)  o  carlos / pass456  (viewer)
3. Navegar por las secciones del sidebar
4. Mostrar que el chat (fragmento) no resetea los filtros del form
5. Demostrar los KPIs en tiempo real

INSTALACIÓN:
   pip install streamlit-authenticator pandas numpy plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import time

st.set_page_config(
    page_title="Plataforma Inmobiliaria IA",
    page_icon="🏡",
    layout="wide"
)

# ─────────────────────────────────────────────────────────
# AUTENTICACIÓN
# ─────────────────────────────────────────────────────────
try:
    import streamlit_authenticator as stauth
    STAUTH_OK = True
except ImportError:
    STAUTH_OK = False

USERS = {
    "ana":    {"name": "Ana García",   "password": "pass123", "role": "admin"},
    "carlos": {"name": "Carlos López", "password": "pass456", "role": "viewer"},
}

def login_simple():
    """Login de respaldo si no está instalado streamlit-authenticator."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Plataforma Inmobiliaria IA")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("Iniciar sesión")
            user = st.text_input("Usuario")
            pw   = st.text_input("Contraseña", type="password")
            if st.button("Entrar", type="primary", use_container_width=True):
                if user in USERS and USERS[user]["password"] == pw:
                    st.session_state.logged_in = True
                    st.session_state["name"]     = USERS[user]["name"]
                    st.session_state["username"] = user
                    st.session_state["role"]     = USERS[user]["role"]
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
            st.caption("Demo: ana/pass123 (admin) · carlos/pass456 (viewer)")
        st.stop()

if STAUTH_OK:
    config = {
        "credentials": {"usernames": {u: {"name": d["name"], "password": d["password"]} for u, d in USERS.items()}},
        "cookie": {"name": "inmobiliaria_final", "key": "secret_2026_modulo4", "expiry_days": 1}
    }
    auth = stauth.Authenticate(config["credentials"], config["cookie"]["name"], config["cookie"]["key"], config["cookie"]["expiry_days"], auto_hash=True)
    auth.login()
    if not st.session_state.get("authentication_status"):
        if st.session_state.get("authentication_status") is False:
            st.error("Credenciales incorrectas")
        st.caption("Demo: ana/pass123 (admin) · carlos/pass456 (viewer)")
        st.stop()
    # Guardar rol
    username = st.session_state.get("username", "")
    st.session_state["role"] = USERS.get(username, {}).get("role", "viewer")
else:
    login_simple()

# ─────────────────────────────────────────────────────────
# SIDEBAR — navegación
# ─────────────────────────────────────────────────────────
nombre = st.session_state.get("name", "Usuario")
rol    = st.session_state.get("role", "viewer")

with st.sidebar:
    st.markdown(f"### 👋 {nombre}")
    st.caption(f"Rol: `{rol}`")

    if STAUTH_OK:
        auth.logout("🚪 Cerrar sesión")
    else:
        if st.button("🚪 Cerrar sesión"):
            st.session_state.logged_in = False
            st.rerun()

    st.divider()
    pagina = st.radio(
        "📂 Navegación",
        ["🔍 Buscador", "📊 Dashboard", "💬 Asistente IA"],
        label_visibility="collapsed"
    )

# ─────────────────────────────────────────────────────────
# DATOS COMPARTIDOS
# ─────────────────────────────────────────────────────────
@st.cache_data
def cargar_propiedades() -> pd.DataFrame:
    np.random.seed(42)
    n = 300
    return pd.DataFrame({
        "id":           range(1, n + 1),
        "nombre":       [f"Propiedad #{i}" for i in range(1, n + 1)],
        "ciudad":       np.random.choice(["Quito", "Guayaquil", "Cuenca"], n),
        "tipo":         np.random.choice(["Casa", "Departamento", "Terreno"], n),
        "precio":       np.random.randint(70_000, 450_000, n),
        "habitaciones": np.random.randint(1, 6, n),
        "area_m2":      np.random.randint(50, 350, n),
        "nueva":        np.random.choice([True, False], n, p=[0.3, 0.7]),
    })

df = cargar_propiedades()

# ─────────────────────────────────────────────────────────
# PÁGINA 1: BUSCADOR
# ─────────────────────────────────────────────────────────
if "🔍" in pagina:
    st.title("🔍 Buscador de Propiedades")

    # ── Formulario de búsqueda ────────────────────────────
    with st.form("busqueda_principal"):
        col1, col2 = st.columns(2)
        ciudad_f   = col1.selectbox("Ciudad", ["Todas", "Quito", "Guayaquil", "Cuenca"])
        tipo_f     = col2.selectbox("Tipo", ["Todos", "Casa", "Departamento", "Terreno"])
        precio_f   = st.slider("Precio máximo ($)", 70_000, 450_000, 250_000, step=10_000)
        col3, col4 = st.columns(2)
        min_hab_f  = col3.number_input("Hab. mínimas", 1, 5, 1)
        solo_new_f = col4.checkbox("Solo propiedades nuevas")
        buscar_f   = st.form_submit_button("🔍 Buscar Propiedades", type="primary")

    if buscar_f or st.session_state.get("ultima_busqueda"):
        # Guardar parámetros de búsqueda para que el chat no los borre
        if buscar_f:
            st.session_state.ultima_busqueda = {
                "ciudad": ciudad_f, "tipo": tipo_f, "precio": precio_f,
                "min_hab": min_hab_f, "solo_new": solo_new_f
            }

        params = st.session_state.ultima_busqueda
        resultado = df.copy()
        if params["ciudad"] != "Todas":
            resultado = resultado[resultado["ciudad"] == params["ciudad"]]
        if params["tipo"] != "Todos":
            resultado = resultado[resultado["tipo"] == params["tipo"]]
        resultado = resultado[resultado["precio"] <= params["precio"]]
        resultado = resultado[resultado["habitaciones"] >= params["min_hab"]]
        if params["solo_new"]:
            resultado = resultado[resultado["nueva"]]

        # Métricas
        m1, m2, m3 = st.columns(3)
        m1.metric("Propiedades encontradas", len(resultado))
        if len(resultado):
            m2.metric("Precio promedio", f"${resultado['precio'].mean():,.0f}")
            m3.metric("Área promedio", f"{resultado['area_m2'].mean():.0f} m²")

        # Tabla
        if len(resultado):
            st.dataframe(
                resultado.sort_values("precio").head(20),
                use_container_width=True, hide_index=True,
                column_config={
                    "precio":   st.column_config.NumberColumn("Precio ($)", format="$%d"),
                    "area_m2":  st.column_config.NumberColumn("Área (m²)", format="%d m²"),
                    "nueva":    st.column_config.CheckboxColumn("Nueva"),
                }
            )

            # ── Panel de acciones (fragmento) ─────────────
            @st.fragment
            def acciones_buscador():
                st.divider()
                sel = st.selectbox(
                    "⭐ Seleccionar para guardar",
                    resultado["nombre"].head(20).tolist(),
                    key="sel_prop"
                )
                c_a, c_b, c_c = st.columns(3)
                if c_a.button("⭐ Guardar favorito", key="fav_b"):
                    st.toast(f"'{sel}' guardado en favoritos!", icon="⭐")
                if c_b.button("📞 Solicitar contacto", key="contact_b"):
                    st.toast("Solicitud enviada al agente", icon="📞")
                if c_c.button("📊 Exportar CSV", key="export_b"):
                    csv = resultado.to_csv(index=False).encode()
                    st.download_button("⬇️ Descargar", csv, "propiedades.csv", "text/csv", key="dl_b")

            acciones_buscador()
        else:
            st.warning("Sin resultados. Ajusta los filtros.")

# ─────────────────────────────────────────────────────────
# PÁGINA 2: DASHBOARD
# ─────────────────────────────────────────────────────────
elif "📊" in pagina:
    st.title("📊 Dashboard Inmobiliario")

    periodo = st.radio("Período", ["7 días", "30 días", "90 días"], horizontal=True)

    @st.cache_data
    def metricas_historicas(p: str) -> pd.DataFrame:
        n = int(p.split()[0])
        np.random.seed(hash(p) % 999)
        fechas = pd.date_range(end=pd.Timestamp.today(), periods=n, freq="D")
        return pd.DataFrame({
            "fecha":   fechas,
            "ventas":  np.random.randint(3, 25, n),
            "leads":   np.random.randint(10, 55, n),
        })

    df_dash = metricas_historicas(periodo)
    st.line_chart(df_dash.set_index("fecha"), use_container_width=True,
                  color=["#FF4B4B", "#3b82f6"])

    @st.fragment(run_every=8)
    def kpis_dash():
        st.caption(f"⚡ Auto-actualización · {time.strftime('%H:%M:%S')}")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Activos ahora", random.randint(10, 40), random.randint(-3, 5))
        k2.metric("Consul/hora",   random.randint(5, 30),  random.randint(-2, 4))
        k3.metric("Conversión",    f"{random.uniform(2,8):.1f}%")
        k4.metric("Precio prom $k", random.randint(90, 160), random.randint(-5, 10))

    kpis_dash()

# ─────────────────────────────────────────────────────────
# PÁGINA 3: ASISTENTE IA (chat en fragmento)
# ─────────────────────────────────────────────────────────
elif "💬" in pagina:
    st.title("💬 Asistente Inmobiliario IA")

    if "chat_app" not in st.session_state:
        st.session_state.chat_app = [
            {"role": "assistant", "content":
             "¡Hola! 🏡 Soy tu asistente inmobiliario. ¿En qué ciudad quieres buscar?"}
        ]

    # Mostrar si hay una búsqueda activa
    if st.session_state.get("ultima_busqueda"):
        p = st.session_state.ultima_busqueda
        st.info(
            f"📋 Búsqueda activa: **{p['ciudad']}** · "
            f"≤ ${p['precio']:,} · {p['min_hab']}+ hab. "
            f"_(Ve al Buscador para cambiarla)_"
        )

    @st.fragment
    def chat_asistente():
        """El chat es un fragmento — no borra los filtros del buscador."""
        container = st.container(height=450)
        with container:
            for msg in st.session_state.chat_app:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        pregunta = st.chat_input("Escribe tu pregunta...")

        if pregunta:
            st.session_state.chat_app.append({"role": "user", "content": pregunta})

            # Respuesta demo
            respuestas_demo = [
                f"Para '{pregunta[:20]}...', encontré opciones interesantes. ¿Quieres que te muestre las primeras 5?",
                "Entendido. El mercado actual tiene buenas oportunidades. ¿Tienes un presupuesto definido?",
                "Esa es una excelente zona. Los precios ahí van de $90k a $280k según el tipo de propiedad.",
                "Te recomiendo también explorar las opciones en Cumbayá y el Valle de los Chillos.",
            ]

            def stream_respuesta():
                texto = random.choice(respuestas_demo)
                for palabra in texto.split():
                    yield palabra + " "
                    time.sleep(0.04)

            with st.chat_message("assistant"):
                respuesta = st.write_stream(stream_respuesta())

            st.session_state.chat_app.append({"role": "assistant", "content": respuesta})
            st.rerun(scope="fragment")

        col_ctrl1, col_ctrl2 = st.columns(2)
        col_ctrl1.caption(f"💬 {len(st.session_state.chat_app)} mensajes")
        if col_ctrl2.button("🗑️ Limpiar chat", key="clr_chat"):
            st.session_state.chat_app = [
                {"role": "assistant", "content": "¡Chat reiniciado! ¿En qué te ayudo?"}
            ]
            st.rerun(scope="fragment")

    chat_asistente()
