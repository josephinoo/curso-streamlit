"""
MÓDULO 4 — BLOQUE 1
Ejercicio 3: Formulario Avanzado — Validación + Cache
======================================================
OBJETIVO: Validar datos del form post-submit y combinar
st.form con @st.cache_data para doble optimización.

INSTRUCCIONES PARA EL PROFESOR:
1. Correr: streamlit run 03_form_avanzado.py
2. Intentar enviar el form con datos inválidos → ver errores
3. Enviar datos válidos → ver el éxito + caché en acción
4. Enviar exactamente los mismos datos → ver que es INSTANTÁNEO
"""

import streamlit as st
import pandas as pd
import numpy as np
import re
import time

st.set_page_config(page_title="Form Avanzado", page_icon="📋", layout="wide")

st.title("📋 Formulario Avanzado: Validación + Caché")
st.caption("Módulo 4 · Bloque 1 · Ejercicio 3")
st.divider()

# ─────────────────────────────────────────────────────────
# PARTE A: Registro de cliente con validación
# ─────────────────────────────────────────────────────────
st.subheader("A) Registro de Cliente — Con Validación")

if "registro_ok" not in st.session_state:
    st.session_state.registro_ok = False
if "clientes" not in st.session_state:
    st.session_state.clientes = []

if not st.session_state.registro_ok:
    with st.form("registro_cliente"):
        col1, col2 = st.columns(2)

        nombre   = col1.text_input("Nombre completo *", placeholder="Ana García")
        email    = col2.text_input("Email *", placeholder="ana@empresa.com")
        telefono = col1.text_input("Teléfono", placeholder="+593 99 123 4567")
        ciudad   = col2.selectbox("Ciudad *", ["Quito", "Guayaquil", "Cuenca"])

        presupuesto = st.select_slider(
            "Rango de presupuesto",
            options=["< $50k", "$50k–$100k", "$100k–$200k", "> $200k"],
            value="$50k–$100k"
        )
        acepta = st.checkbox("Acepto los términos y condiciones *")

        enviado = st.form_submit_button("📝 Registrar Cliente", type="primary")

    if enviado:
        # Validación DESPUÉS del submit
        errores = []
        if not nombre.strip():
            errores.append("El nombre completo es requerido")
        elif len(nombre.strip()) < 3:
            errores.append("El nombre debe tener al menos 3 caracteres")
        if not email.strip():
            errores.append("El email es requerido")
        elif not re.match(r'^[\w.+-]+@[\w-]+\.\w{2,}$', email):
            errores.append("El email no tiene formato válido (ej: usuario@dominio.com)")
        if not acepta:
            errores.append("Debes aceptar los términos y condiciones")

        if errores:
            for e in errores:
                st.error(f"❌ {e}")
            st.info("💡 Corrige los errores y vuelve a enviar el formulario")
        else:
            st.session_state.clientes.append({
                "nombre": nombre, "email": email,
                "ciudad": ciudad, "presupuesto": presupuesto
            })
            st.session_state.registro_ok = True
            st.rerun()
else:
    ultimo = st.session_state.clientes[-1]
    st.success(f"✅ ¡{ultimo['nombre']} registrado correctamente en {ultimo['ciudad']}!")
    st.balloons()
    if st.button("➕ Registrar otro cliente"):
        st.session_state.registro_ok = False
        st.rerun()

if st.session_state.clientes:
    with st.expander(f"📋 Ver clientes registrados ({len(st.session_state.clientes)})"):
        st.dataframe(pd.DataFrame(st.session_state.clientes), use_container_width=True, hide_index=True)

st.divider()

# ─────────────────────────────────────────────────────────
# PARTE B: Doble optimización — form + cache_data
# ─────────────────────────────────────────────────────────
st.subheader("B) Doble Optimización: st.form + @st.cache_data")

st.info(
    "**Doble optimización:**\n"
    "1. `st.form` → 0 reruns mientras configuras filtros\n"
    "2. `@st.cache_data` → si repites la misma búsqueda, es **instantáneo**"
)

@st.cache_data(show_spinner=False)
def cargar_propiedades() -> pd.DataFrame:
    """Carga UNA sola vez — simula leer un CSV grande."""
    np.random.seed(99)
    n = 500
    return pd.DataFrame({
        "ciudad":       np.random.choice(["Quito","Guayaquil","Cuenca"], n),
        "tipo":         np.random.choice(["Casa","Departamento","Terreno"], n),
        "precio":       np.random.randint(60_000, 500_000, n),
        "habitaciones": np.random.randint(1, 6, n),
        "area_m2":      np.random.randint(50, 400, n),
    })

@st.cache_data(show_spinner=False)
def filtrar_propiedades(ciudad: str, precio_max: int, min_hab: int, tipo: str) -> pd.DataFrame:
    """
    Cache por combinación de parámetros.
    Si se repite la misma búsqueda, retorna instantáneo.
    """
    df = cargar_propiedades()
    result = df.copy()
    if ciudad != "Todas":
        result = result[result["ciudad"] == ciudad]
    if tipo != "Todos":
        result = result[result["tipo"] == tipo]
    result = result[result["precio"] <= precio_max]
    result = result[result["habitaciones"] >= min_hab]
    time.sleep(1.5)  # Simula consulta pesada a DB
    return result

with st.form("filtros_cache"):
    c1, c2, c3 = st.columns(3)
    ciudad_b    = c1.selectbox("Ciudad", ["Todas", "Quito", "Guayaquil", "Cuenca"], key="cb")
    tipo_b      = c2.selectbox("Tipo", ["Todos", "Casa", "Departamento", "Terreno"], key="tb")
    precio_b    = c3.slider("Precio máx ($)", 60_000, 500_000, 250_000, step=10_000, key="pb")
    min_hab_b   = st.number_input("Hab. mínimas", 1, 5, 1, key="hb")
    buscar_b    = st.form_submit_button("🔍 Buscar (prueba 2 veces con los mismos filtros)", type="primary")

if buscar_b:
    t_inicio = time.time()

    with st.spinner("Consultando..."):
        resultado_b = filtrar_propiedades(ciudad_b, precio_b, min_hab_b, tipo_b)

    t_fin = time.time()
    elapsed = t_fin - t_inicio

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Propiedades", len(resultado_b))
    col_m2.metric("Precio prom.", f"${resultado_b['precio'].mean():,.0f}" if len(resultado_b) else "-")
    col_m3.metric(
        "Tiempo de respuesta",
        f"{elapsed:.2f}s",
        delta="desde caché ⚡" if elapsed < 0.1 else "consulta nueva 🔄",
        delta_color="normal" if elapsed < 0.1 else "off"
    )

    if elapsed < 0.1:
        st.success("⚡ ¡Resultado desde caché! Sin consultar la DB.")
    else:
        st.info("🔄 Búsqueda nueva procesada. Prueba los mismos filtros otra vez.")

    st.dataframe(resultado_b.head(10), use_container_width=True, hide_index=True)
