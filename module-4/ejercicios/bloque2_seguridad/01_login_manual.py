"""
MÓDULO 4 — BLOQUE 2
Ejercicio 1: st.secrets + Login Manual con session_state
=========================================================
OBJETIVO: Implementar un login básico usando st.secrets para
las credenciales y st.stop() para bloquear el acceso.

INSTRUCCIONES PARA EL PROFESOR:
1. Primero crear .streamlit/secrets.toml con:
      USUARIO_ADMIN = "admin"
      CLAVE_ADMIN   = "clave123"
2. Correr: streamlit run 01_login_manual.py
3. Probar credenciales incorrectas → ver error
4. Probar credenciales correctas → acceder al dashboard
5. Observar cómo st.stop() bloquea todo el contenido

CREDENCIALES DE PRUEBA (para la demo sin secrets.toml):
   Usuario: admin
   Contraseña: clave123
"""

import streamlit as st

st.set_page_config(page_title="Login Manual", page_icon="🔐")

# ─────────────────────────────────────────────────────────
# LEER CREDENCIALES — con fallback para demo sin secrets.toml
# ─────────────────────────────────────────────────────────
try:
    USUARIO_OK = st.secrets["USUARIO_ADMIN"]
    CLAVE_OK   = st.secrets["CLAVE_ADMIN"]
    usando_secrets = True
except (FileNotFoundError, KeyError):
    # Fallback para demo sin archivo secrets.toml
    USUARIO_OK = "admin"
    CLAVE_OK   = "clave123"
    usando_secrets = False

# ─────────────────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = None

# ─────────────────────────────────────────────────────────
# PANTALLA DE LOGIN (si no está autenticado)
# ─────────────────────────────────────────────────────────
if not st.session_state.autenticado:

    # Centrar el formulario
    col_vacio1, col_form, col_vacio2 = st.columns([1, 2, 1])

    with col_form:
        st.markdown("## 🔐 Acceso Restringido")

        if not usando_secrets:
            st.warning(
                "**Modo demo** — sin secrets.toml.\n\n"
                "Credenciales: `admin` / `clave123`"
            )

        usuario = st.text_input("👤 Usuario", placeholder="admin")
        clave   = st.text_input("🔑 Contraseña", type="password", placeholder="••••••••")

        if st.button("Ingresar →", type="primary", use_container_width=True):
            if usuario == USUARIO_OK and clave == CLAVE_OK:
                st.session_state.autenticado    = True
                st.session_state.usuario_actual = usuario
                st.rerun()
            elif not usuario:
                st.error("❌ Ingresa tu usuario")
            elif not clave:
                st.error("❌ Ingresa tu contraseña")
            else:
                st.error("❌ Credenciales incorrectas. Intenta de nuevo.")

        st.caption("Pista: el usuario es **admin** y la contraseña **clave123**")

    # ← MÁGICO: nada de lo que sigue se ejecuta
    st.stop()

# ─────────────────────────────────────────────────────────
# CONTENIDO PROTEGIDO (solo si está autenticado)
# ─────────────────────────────────────────────────────────
# Si llegamos aquí, el usuario está autenticado

st.title(f"🏠 Dashboard — Bienvenido, {st.session_state.usuario_actual}!")

col_info, col_logout = st.columns([3, 1])
with col_info:
    if usando_secrets:
        st.success("✅ Credenciales cargadas desde `.streamlit/secrets.toml`")
    else:
        st.info("ℹ️ Modo demo — en producción usar `st.secrets`")
with col_logout:
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.autenticado    = False
        st.session_state.usuario_actual = None
        st.rerun()

st.divider()

# Contenido del dashboard
st.subheader("📊 Datos Privados (solo para usuarios autenticados)")

import pandas as pd, numpy as np
np.random.seed(1)
df_privado = pd.DataFrame({
    "Propiedad": [f"Casa #{i}" for i in range(1, 6)],
    "Precio ($)": np.random.randint(80_000, 300_000, 5),
    "Ciudad":     ["Quito", "Guayaquil", "Cuenca", "Quito", "Guayaquil"],
    "Estado":     ["Disponible", "Vendida", "Disponible", "Reservada", "Disponible"],
})
st.dataframe(df_privado, use_container_width=True, hide_index=True)

st.divider()
with st.expander("📚 ¿Cómo funciona? — Explicación del código"):
    st.code("""
# 1. Verificar si está autenticado
if not st.session_state.autenticado:
    # mostrar login...
    st.stop()  # ← TODO lo que viene después NO se ejecuta

# 2. Solo llega aquí si autenticado = True
st.title("Dashboard Privado")
df = cargar_datos_privados()  # ← NUNCA corre si no está autenticado
    """, language="python")
    st.markdown("""
    **Puntos clave:**
    - `st.secrets` lee `.streamlit/secrets.toml` automáticamente
    - `st.stop()` detiene la ejecución del script **completamente** — no es solo CSS
    - `st.session_state.autenticado` persiste entre re-runs
    - `st.rerun()` fuerza una nueva ejecución desde arriba
    """)
