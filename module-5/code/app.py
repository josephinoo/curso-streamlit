import streamlit as st
from auth import show_login

# 1. Configuración global (Solo se necesita aquí)
st.set_page_config(
    page_title="RetailDash",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

# 2. Control de sesión inicial
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username  = ""
    st.session_state.nombre    = ""
    st.session_state.rol       = ""

# 3. Definición de las páginas del Dashboard
#    Aquí listamos las páginas de la carpeta /pages pero sin incluir 'app.py'
dashboard_pages = [
    st.Page("pages/1_Resumen.py", title="Resumen", icon="📊", default=True),
    st.Page("pages/2_Ventas.py", title="Ventas", icon="💰"),
    st.Page("pages/3_Geografico.py", title="Geográfico", icon="🗺️"),
    st.Page("pages/4_Datos.py", title="Datos", icon="📁"),
]

# 4. Lógica de Routing con st.navigation
if not st.session_state.logged_in:
    # Si NO está logueado:
    # - Creamos una navegación con una página temporal que llama a show_login
    # - Usamos position="hidden" para que no se vea nada en la barra lateral
    pg = st.navigation([st.Page(show_login, title="Login")], position="hidden")
    pg.run()
else:
    # Si SÍ está logueado:
    # - Mostramos las páginas del dashboard
    # - Streamlit ocultará automáticamente el archivo 'app.py' del menú
    pg = st.navigation(dashboard_pages)
    pg.run()
