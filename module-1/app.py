import streamlit as st
import random

st.title("Mini Dashabord de datos")
st.caption("Ejemplo basico de un dashabord de datos con Streamlit")
st.divider()

st.header("Configuracion")
col1, col2 = st.columns(2,border=True)
with col1:
    cantidad = st.slider("Cantidad de datos",min_value=10, max_value=50)
with col2:
    mostrar_detalle = st.checkbox("Mostrar detalle")

# generar datos aleatorios
datos = []
for i in range(cantidad):
    dato = random.randint(1, 1000)
    datos.append(dato)

total = sum(datos)
promedio = total/cantidad
maximo = max(datos)

if mostrar_detalle == True:
    st.write(datos)

st.header("Metricas")
c1, c2, c3 = st.columns(3,border=True)
with c1:
    st.metric("Total", total)
with c2:
    st.metric("Promedio",promedio)
with c3:
    st.metric("Maximo",maximo)

if promedio > 500:
    st.success("El promedio es alto")
if promedio < 500:
    st.warning("El promedio es bajo")

celebrar = st.button("Celebrar")
if celebrar:
    st.balloons()