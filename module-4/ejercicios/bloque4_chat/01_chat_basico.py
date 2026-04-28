"""
MÓDULO 4 — BLOQUE 4
Ejercicio 1: Chat Básico con Historial Persistente
===================================================
OBJETIVO: Construir una interfaz de chat con st.chat_message,
st.chat_input y session_state para mantener el historial.

INSTRUCCIONES PARA EL PROFESOR:
1. Correr: streamlit run 01_chat_basico.py
2. Primero mostrar el chat SIN guardar en session_state (comentar la lista)
   → el historial se borra en cada mensaje
3. Mostrar con session_state → el historial persiste
4. Demostrar el efecto de streaming con st.write_stream
"""

import streamlit as st
import time
import random

st.set_page_config(page_title="Chat Básico", page_icon="💬")

st.title("💬 Chat Básico con Historial")
st.caption("Módulo 4 · Bloque 4 · Ejercicio 1")

# ─────────────────────────────────────────────────────────
# MODO DE DEMOSTRACIÓN: permite mostrar con/sin session_state
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("⚙️ Modo demostración")
    usar_historial = st.toggle(
        "Guardar historial en session_state",
        value=True,
        help="Desactívalo para ver qué pasa sin session_state"
    )
    usar_streaming = st.toggle(
        "Efecto streaming (typewriter)",
        value=True,
        help="Simula el efecto de escritura de ChatGPT"
    )
    velocidad = st.slider(
        "Velocidad streaming (seg/palabra)",
        0.01, 0.15, 0.04, step=0.01
    )
    st.divider()
    st.caption("**Atajos:**")
    st.caption("• Sin historial: el chat olvida todo en cada mensaje")
    st.caption("• Con historial: la conversación persiste")

# ─────────────────────────────────────────────────────────
# INICIALIZAR HISTORIAL
# ─────────────────────────────────────────────────────────
if "chat_historial" not in st.session_state:
    st.session_state.chat_historial = [
        {
            "role":    "assistant",
            "content": "¡Hola! 🏠 Soy tu asesor inmobiliario virtual. "
                       "¿Qué tipo de propiedad estás buscando hoy?"
        }
    ]

# ─────────────────────────────────────────────────────────
# FUNCIÓN DE RESPUESTA
# ─────────────────────────────────────────────────────────
def generar_respuesta(pregunta: str) -> str:
    """Genera una respuesta de demostración basada en palabras clave."""
    pregunta_lower = pregunta.lower()

    if any(w in pregunta_lower for w in ["quito", "guayaquil", "cuenca"]):
        ciudad = next(c for c in ["Quito", "Guayaquil", "Cuenca"] if c.lower() in pregunta_lower)
        return (
            f"¡Excelente elección! {ciudad} tiene muy buenas opciones disponibles. "
            f"Actualmente hay {random.randint(15, 45)} propiedades que coinciden "
            f"con criterios típicos. Los precios van desde $80,000 hasta $350,000 "
            f"dependiendo de la zona y las características."
        )
    elif any(w in pregunta_lower for w in ["precio", "costo", "valor", "cuánto"]):
        return (
            "Los precios varían mucho según la ciudad y el tipo de propiedad. "
            f"El precio promedio actual es ${random.randint(120, 180)},000. "
            "¿En qué ciudad estás interesado? Puedo darte información más específica."
        )
    elif any(w in pregunta_lower for w in ["hab", "dormitorio", "cuarto"]):
        return (
            f"Tengo opciones con 1, 2, 3 y hasta 4 habitaciones. "
            f"Las propiedades de {random.randint(2,3)} habitaciones son las más populares. "
            "¿Cuántas habitaciones necesitas y cuál es tu presupuesto aproximado?"
        )
    elif any(w in pregunta_lower for w in ["hola", "buenos", "buenas"]):
        return "¡Hola! 😊 Estoy aquí para ayudarte a encontrar tu propiedad ideal. ¿Por dónde empezamos?"
    else:
        opciones = [
            f"Interesante! Basándome en '{pregunta[:20]}...', puedo mostrarte opciones en Quito, Guayaquil o Cuenca. ¿Cuál prefieres?",
            "Entendido. Para darte las mejores recomendaciones, ¿cuál es tu presupuesto aproximado?",
            f"He registrado tu consulta: '{pregunta[:30]}'. ¿Te gustaría ver propiedades disponibles ahora mismo?",
        ]
        return random.choice(opciones)


def respuesta_stream(texto: str, velocidad: float):
    """Generador para el efecto de escritura palabra a palabra."""
    for palabra in texto.split():
        yield palabra + " "
        time.sleep(velocidad)


# ─────────────────────────────────────────────────────────
# RENDERIZAR HISTORIAL
# ─────────────────────────────────────────────────────────
if usar_historial:
    mensajes_a_mostrar = st.session_state.chat_historial
else:
    # Sin session_state: solo el mensaje de bienvenida (se pierde todo)
    mensajes_a_mostrar = [st.session_state.chat_historial[0]]
    if len(st.session_state.chat_historial) > 1:
        st.warning("⚠️ Sin `session_state`, el historial anterior se pierde en cada rerun")

for msg in mensajes_a_mostrar:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────────────────
# INPUT DEL USUARIO
# ─────────────────────────────────────────────────────────
pregunta = st.chat_input("Escribe tu consulta inmobiliaria...")

if pregunta:
    # 1. Guardar y mostrar mensaje del usuario
    if usar_historial:
        st.session_state.chat_historial.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    # 2. Generar respuesta
    texto_respuesta = generar_respuesta(pregunta)

    # 3. Mostrar respuesta (con o sin streaming)
    with st.chat_message("assistant"):
        if usar_streaming:
            respuesta = st.write_stream(respuesta_stream(texto_respuesta, velocidad))
        else:
            st.markdown(texto_respuesta)
            respuesta = texto_respuesta

    # 4. Guardar respuesta en historial
    if usar_historial:
        st.session_state.chat_historial.append({"role": "assistant", "content": respuesta})

# ─────────────────────────────────────────────────────────
# CONTROLES EN SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.divider()
    n_msgs = len(st.session_state.chat_historial)
    st.metric("Mensajes en historial", n_msgs)
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.chat_historial = [
            {"role": "assistant", "content": "¡Conversación reiniciada! ¿En qué te ayudo?"}
        ]
        st.rerun()

    if st.toggle("Ver historial completo (debug)"):
        st.json(st.session_state.chat_historial)
