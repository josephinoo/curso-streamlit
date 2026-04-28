"""
MÓDULO 4 — BLOQUE 2
Ejercicio 3: Control de Roles (RBAC)
=====================================
OBJETIVO: Implementar Role-Based Access Control.
Distintos roles ven distintas secciones de la app.

INSTRUCCIONES PARA EL PROFESOR:
1. Correr: streamlit run 03_roles_rbac.py
2. Hacer login con diferentes usuarios y mostrar
   que cada rol ve una interfaz distinta
3. Explicar el decorador require_role()

USUARIOS (sin contraseña real — demo simplificada):
   Seleccionar rol desde un selectbox de demostración
"""

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="RBAC — Control de Roles", page_icon="🛡️", layout="wide")

st.title("🛡️ Control de Roles (RBAC)")
st.caption("Módulo 4 · Bloque 2 · Ejercicio 3")
st.divider()

# ─────────────────────────────────────────────────────────
# DECORADOR require_role
# ─────────────────────────────────────────────────────────
def require_role(roles: list):
    """
    Decorador para proteger funciones según el rol del usuario.
    Uso: @require_role(["admin"])
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_role = st.session_state.get("demo_role", None)
            if current_role not in roles:
                st.error(f"🚫 **Acceso denegado.** Necesitas uno de estos roles: `{roles}`")
                st.info(f"Tu rol actual: `{current_role}` — Cambia el rol en el sidebar")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ─────────────────────────────────────────────────────────
# SIMULAR LOGIN CON ROLES (en producción usarías stauth)
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("🧪 Simular login")
    st.caption("En producción esto lo maneja streamlit-authenticator")

    rol_demo = st.selectbox(
        "Selecciona tu rol",
        ["admin", "editor", "viewer"],
        help="Cambia el rol para ver qué acceso tiene cada uno"
    )
    st.session_state["demo_role"] = rol_demo

    nombre_demo = {"admin": "Ana García", "editor": "Carlos López", "viewer": "María Torres"}
    st.markdown(f"**Usuario:** {nombre_demo[rol_demo]}")
    st.markdown(f"**Rol:** `{rol_demo}`")

    st.divider()
    st.markdown("**Permisos por rol:**")
    permisos = {
        "admin":  ["Ver dashboard", "Editar propiedades", "Gestionar usuarios", "Ver reportes"],
        "editor": ["Ver dashboard", "Editar propiedades", "Ver reportes"],
        "viewer": ["Ver dashboard"],
    }
    for p in permisos[rol_demo]:
        st.markdown(f"✅ {p}")
    roles_sin_permiso = set(permisos["admin"]) - set(permisos[rol_demo])
    for p in roles_sin_permiso:
        st.markdown(f"🚫 {p}")

# ─────────────────────────────────────────────────────────
# CONTENT — acceso controlado por rol
# ─────────────────────────────────────────────────────────
rol = st.session_state.get("demo_role", "viewer")
nombre = {"admin": "Ana García", "editor": "Carlos López", "viewer": "María Torres"}[rol]

st.markdown(f"### 👋 Hola, {nombre} — Rol: `{rol}`")

# ── Sección 1: Dashboard (todos los roles) ─────────────────
st.subheader("📊 Dashboard — Visible para todos")
np.random.seed(42)
c1, c2, c3 = st.columns(3)
c1.metric("Propiedades activas", 127)
c2.metric("Ventas este mes", "$1.2M")
c3.metric("Visitas web", "4,832")

# ── Sección 2: Edición (admin y editor) ────────────────────
st.divider()
st.subheader("✏️ Edición de Propiedades")

@require_role(["admin", "editor"])
def panel_edicion():
    st.success("✅ Tienes permiso para editar")
    with st.form("editar_propiedad"):
        col_a, col_b = st.columns(2)
        nombre_prop = col_a.text_input("Nombre propiedad", "Casa Norte #42")
        precio      = col_b.number_input("Precio ($)", 50000, 500000, 150000)
        descripcion = st.text_area("Descripción", "Hermosa casa de 3 dormitorios...")
        if st.form_submit_button("💾 Guardar cambios", type="primary"):
            st.success(f"Propiedad '{nombre_prop}' actualizada — ${precio:,}")

panel_edicion()

# ── Sección 3: Gestión de usuarios (solo admin) ─────────────
st.divider()
st.subheader("👥 Gestión de Usuarios")

@require_role(["admin"])
def panel_usuarios():
    st.success("✅ Acceso de administrador")
    df_usuarios = pd.DataFrame({
        "Usuario": ["ana", "carlos", "maria"],
        "Nombre":  ["Ana García", "Carlos López", "María Torres"],
        "Rol":     ["admin", "editor", "viewer"],
        "Email":   ["ana@empresa.com", "carlos@empresa.com", "maria@empresa.com"],
    })
    st.dataframe(df_usuarios, use_container_width=True, hide_index=True)

    col_u1, col_u2 = st.columns(2)
    if col_u1.button("➕ Agregar usuario"):
        st.info("Aquí iría el formulario de creación")
    if col_u2.button("🗑️ Eliminar usuario", type="secondary"):
        st.warning("Confirmación requerida")

panel_usuarios()

# ── Sección 4: Reportes (admin y editor) ────────────────────
st.divider()
st.subheader("📈 Reportes")

@require_role(["admin", "editor"])
def panel_reportes():
    st.success("✅ Tienes acceso a reportes")
    df_rep = pd.DataFrame({
        "Mes":    ["Ene","Feb","Mar","Abr","May"],
        "Ventas": np.random.randint(50, 200, 5),
        "Meta":   [120] * 5,
    })
    st.bar_chart(df_rep.set_index("Mes"))

panel_reportes()
