import streamlit as st

# ─── Usuarios hardcodeados (demo para principiantes) ─────────────────────────
USUARIOS = {
    "admin":  {"password": "admin123",   "nombre": "Administrador", "rol": "Admin"},
    "ana":    {"password": "ana2024",    "nombre": "Ana García",    "rol": "Analista"},
    "carlos": {"password": "carlos2024", "nombre": "Carlos López",  "rol": "Viewer"},
}


def verificar_credenciales(usuario: str, password: str) -> bool:
    if usuario in USUARIOS:
        return USUARIOS[usuario]["password"] == password
    return False


def show_login():
    # Centrar con columnas
    _, col, _ = st.columns([1, 1.5, 1])

    with col:
        st.title("RetailDash")
        st.subheader("Iniciar sesión")
        st.caption("Dashboard de Ventas · Módulo 5")
        st.divider()

        # st.form evita que la app se recargue al escribir
        with st.form("login_form"):
            usuario  = st.text_input("Usuario",    placeholder="Ej: admin")
            password = st.text_input("Contraseña", placeholder="••••••••", type="password")
            submit   = st.form_submit_button("Iniciar sesión", use_container_width=True, type="primary")

        # Validación al hacer submit
        if submit:
            if not usuario or not password:
                st.warning("Completa todos los campos.")
            elif verificar_credenciales(usuario.strip().lower(), password):
                st.session_state.logged_in = True
                st.session_state.username  = usuario.strip().lower()
                st.session_state.nombre    = USUARIOS[usuario.strip().lower()]["nombre"]
                st.session_state.rol       = USUARIOS[usuario.strip().lower()]["rol"]
                st.success("¡Bienvenido/a! Cargando dashboard...")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

        st.divider()
        st.info("**Usuarios demo:** admin / admin123 · ana / ana2024 · carlos / carlos2024")
