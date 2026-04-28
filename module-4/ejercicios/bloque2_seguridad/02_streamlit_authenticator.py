"""
MÓDULO 4 — BLOQUE 2
Ejercicio 2: streamlit-authenticator — Multi-usuario
=====================================================
OBJETIVO: Usar streamlit-authenticator para login multi-usuario
con contraseñas hasheadas, cookies persistentes y logout.

INSTALACIÓN REQUERIDA:
   pip install streamlit-authenticator

INSTRUCCIONES PARA EL PROFESOR:
1. Instalar: pip install streamlit-authenticator
2. Correr: streamlit run 02_streamlit_authenticator.py
3. Probar con: ana / pass123  o  carlos / pass456
4. Mostrar el logout en el sidebar
5. Cerrar el navegador y volver → la cookie mantiene la sesión

USUARIOS DE PRUEBA:
   - ana       / pass123   (rol: admin)
   - carlos    / pass456   (rol: viewer)
"""

import streamlit as st

# ── Verificar instalación ─────────────────────────────────
try:
    import streamlit_authenticator as stauth
except ImportError:
    st.error("❌ **streamlit-authenticator no está instalado.**")
    st.code("pip install streamlit-authenticator", language="bash")
    st.stop()

st.set_page_config(page_title="streamlit-authenticator", page_icon="🏆")

# ─────────────────────────────────────────────────────────
# CONFIGURACIÓN DE USUARIOS
# En producción: leer desde st.secrets o base de datos
# ─────────────────────────────────────────────────────────

# Las contraseñas DEBEN estar hasheadas con bcrypt
# Para generar hashes: stauth.Hasher(['pass123']).generate()
# DEMO: usamos auto_hash=True para que hashee automáticamente

config = {
    "credentials": {
        "usernames": {
            "ana": {
                "name":     "Ana García",
                "email":    "ana@empresa.com",
                "password": "pass123",   # auto_hash=True lo hashea
                "role":     "admin",
            },
            "carlos": {
                "name":     "Carlos López",
                "email":    "carlos@empresa.com",
                "password": "pass456",
                "role":     "viewer",
            },
        }
    },
    "cookie": {
        "name":        "modulo4_cookie",
        "key":         "clave_firma_muy_secreta_2026",  # en prod: st.secrets["JWT_SECRET"]
        "expiry_days": 1,
    },
}

# ─────────────────────────────────────────────────────────
# CREAR AUTENTICADOR
# ─────────────────────────────────────────────────────────
auth = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    auto_hash=True,   # hashea las contraseñas en texto plano automáticamente
)

# ─────────────────────────────────────────────────────────
# RENDERIZAR WIDGET DE LOGIN
# ─────────────────────────────────────────────────────────
auth.login()

# ─────────────────────────────────────────────────────────
# MANEJAR ESTADO DE AUTENTICACIÓN
# ─────────────────────────────────────────────────────────
status = st.session_state.get("authentication_status")

if status is True:
    # ── Usuario autenticado ───────────────────────────────
    nombre   = st.session_state["name"]
    username = st.session_state["username"]
    role     = config["credentials"]["usernames"][username]["role"]

    # Guardar rol en session_state para usar en toda la app
    st.session_state["role"] = role

    # Logout en el sidebar
    with st.sidebar:
        st.markdown(f"### 👋 Hola, {nombre}")
        st.caption(f"Usuario: `{username}` · Rol: `{role}`")
        auth.logout("🚪 Cerrar sesión")
        st.divider()

    # ── Contenido según rol ───────────────────────────────
    st.title(f"🏠 Dashboard — {nombre}")

    if role == "admin":
        st.success("🔑 **Modo Administrador** — Acceso completo")
        tabs = st.tabs(["📊 Dashboard", "⚙️ Gestión", "👥 Usuarios"])
    else:
        st.info("👁️ **Modo Viewer** — Solo lectura")
        tabs = st.tabs(["📊 Dashboard"])

    with tabs[0]:
        st.subheader("📊 Métricas Principales")
        import pandas as pd, numpy as np
        np.random.seed(42)
        col1, col2, col3 = st.columns(3)
        col1.metric("Propiedades activas", 127, delta="+5")
        col2.metric("Ventas este mes", "$1.2M", delta="+12%")
        col3.metric("Clientes registrados", 483, delta="+23")

        df = pd.DataFrame({
            "Mes":    ["Ene","Feb","Mar","Abr","May","Jun"],
            "Ventas": np.random.randint(80, 200, 6),
            "Leads":  np.random.randint(30, 80, 6),
        })
        st.line_chart(df.set_index("Mes"))

    if role == "admin" and len(tabs) > 1:
        with tabs[1]:
            st.subheader("⚙️ Panel de Gestión (solo admin)")
            st.warning("Esta sección solo es visible para administradores")
            st.dataframe(pd.DataFrame({
                "Usuario": ["ana", "carlos"],
                "Rol": ["admin", "viewer"],
                "Email": ["ana@empresa.com", "carlos@empresa.com"],
                "Último acceso": ["Hoy", "Ayer"],
            }), use_container_width=True, hide_index=True)

        with tabs[2]:
            st.subheader("👥 Gestión de Usuarios")
            st.info("Aquí iría la interfaz para agregar/eliminar usuarios")

elif status is False:
    st.error("❌ Usuario o contraseña incorrectos")
    st.caption("Prueba con: **ana** / **pass123** o **carlos** / **pass456**")

elif status is None:
    st.warning("👆 Ingresa tus credenciales para acceder")
    st.caption("Usuarios disponibles: **ana** (admin) y **carlos** (viewer)")

# ── Instrucción de hasheo ─────────────────────────────────
with st.expander("🔒 ¿Cómo hashear contraseñas para producción?"):
    st.code("""
import streamlit_authenticator as stauth

# Generar hashes para guardar en secrets.toml
hashed = stauth.Hasher(['pass123', 'pass456']).generate()
print(hashed)
# → ['$2b$12$abc...', '$2b$12$xyz...']

# Verificar si un string ya es hash
print(stauth.Hasher.is_hash('$2b$12$abc...'))  # → True
    """, language="python")
    st.markdown("**Luego guarda los hashes en `.streamlit/secrets.toml`** (nunca el texto plano)")
