"""
MÓDULO 4 — BLOQUE 4
Ejercicio 2: Chat con System Prompt + OpenAI Real
==================================================
OBJETIVO: Conectar el chat a OpenAI con system prompt,
gestionar el historial completo y usar stream=True.

MODOS DE OPERACIÓN:
  - Sin API key → modo demostración (respuestas ficticias)
  - Con API key en secrets.toml → respuestas reales de GPT-4o-mini

INSTRUCCIONES PARA EL PROFESOR:
1. Correr: streamlit run 02_chat_openai.py
2. Mostrar primero sin API key (modo demo)
3. Si tienes API key, agregar a secrets.toml:
      OPENAI_KEY = "sk-proj-..."
4. Reiniciar la app → respuestas reales con streaming

CONFIGURACIÓN secrets.toml (opcional):
   OPENAI_KEY = "sk-proj-tu-clave-aqui"
"""

import streamlit as st
import time
import random

st.set_page_config(
    page_title="Chat + OpenAI",
    page_icon="🤖",
    layout="wide"
)

# ─────────────────────────────────────────────────────────
# DETECTAR SI TENEMOS OPENAI
# ─────────────────────────────────────────────────────────
try:
    from openai import OpenAI
    OPENAI_DISPONIBLE = True
except ImportError:
    OPENAI_DISPONIBLE = False

try:
    OPENAI_KEY = st.secrets["OPENAI_KEY"]
    TIENE_KEY  = True
except (FileNotFoundError, KeyError):
    OPENAI_KEY = None
    TIENE_KEY  = False

MODO_REAL = OPENAI_DISPONIBLE and TIENE_KEY

# ─────────────────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Eres un asesor inmobiliario experto en el mercado ecuatoriano.
Tienes amplio conocimiento sobre propiedades en Quito, Guayaquil y Cuenca.
Responde siempre en español, de manera concisa y profesional.
Cuando el usuario pregunta por propiedades, pide sus filtros principales:
ciudad, presupuesto y número de habitaciones antes de dar recomendaciones.
Si no tienes información suficiente, pregunta para dar mejores resultados.
Sé amable y orientado a soluciones."""

# ─────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("⚙️ Configuración")

    if MODO_REAL:
        st.success("✅ OpenAI conectado — respuestas reales")
        modelo = st.selectbox("Modelo", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
        max_tokens = st.slider("Max tokens respuesta", 100, 1000, 400)
        temperatura = st.slider("Temperatura (creatividad)", 0.0, 1.0, 0.7, 0.1)
    else:
        st.warning(
            "⚠️ **Modo demo** — sin OpenAI\n\n"
            "Para respuestas reales:\n"
            "1. `pip install openai`\n"
            "2. Agregar `OPENAI_KEY` a `secrets.toml`"
        )
        modelo = "demo"
        max_tokens = 400
        temperatura = 0.7

    st.divider()
    st.caption("**System Prompt activo:**")
    with st.expander("Ver prompt"):
        st.text(SYSTEM_PROMPT)

    st.divider()
    n_hist = len([m for m in st.session_state.get("oai_historial", []) if m["role"] != "system"])
    st.metric("Mensajes en contexto", n_hist)
    st.caption("⚠️ Cada mensaje se envía a la API — controla el costo")

    if st.button("🗑️ Nueva conversación"):
        st.session_state.oai_historial = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

# ─────────────────────────────────────────────────────────
# INICIALIZAR HISTORIAL
# ─────────────────────────────────────────────────────────
if "oai_historial" not in st.session_state:
    st.session_state.oai_historial = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ─────────────────────────────────────────────────────────
# FUNCIONES DE RESPUESTA
# ─────────────────────────────────────────────────────────
def respuesta_demo_stream(pregunta: str):
    """Genera respuesta de demostración con efecto streaming."""
    respuestas = [
        f"¡Claro! Para '{pregunta[:20]}...', te puedo ayudar. ¿En qué ciudad prefieres buscar?",
        "Entendido. El mercado inmobiliario en Ecuador tiene muy buenas opciones ahora. "
        "Los precios en Quito van desde $90,000 para departamentos hasta $400,000 para casas grandes.",
        "Perfecto. Con ese presupuesto tienes varias opciones disponibles. "
        "Te recomiendo explorar sectores como Cumbayá o Valle de los Chillos en Quito.",
        f"Basándome en tu consulta: '{pregunta[:25]}', hay aproximadamente "
        f"{random.randint(10, 50)} propiedades disponibles que coinciden.",
    ]
    texto = random.choice(respuestas)
    for palabra in texto.split():
        yield palabra + " "
        time.sleep(0.04)

def respuesta_openai_stream(historial: list, modelo: str, max_tok: int, temp: float):
    """Genera respuesta real de OpenAI con streaming."""
    client  = OpenAI(api_key=OPENAI_KEY)
    stream  = client.chat.completions.create(
        model=modelo,
        messages=historial,
        max_tokens=max_tok,
        temperature=temp,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content

# ─────────────────────────────────────────────────────────
# UI PRINCIPAL
# ─────────────────────────────────────────────────────────
st.title("🤖 Asistente Inmobiliario IA")
st.caption(
    f"{'🟢 OpenAI ' + modelo if MODO_REAL else '🟡 Modo demo'} · "
    f"Módulo 4 · Bloque 4 · Ejercicio 2"
)

# Renderizar historial (sin el system prompt)
for msg in st.session_state.oai_historial:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Mensaje de bienvenida si el historial está vacío
if len(st.session_state.oai_historial) == 1:
    with st.chat_message("assistant"):
        st.markdown(
            "¡Hola! 🏡 Soy tu asesor inmobiliario virtual. "
            "Puedo ayudarte a encontrar la propiedad ideal en Ecuador. "
            "¿Por dónde quieres empezar?"
        )

# ─────────────────────────────────────────────────────────
# CAPTURAR INPUT
# ─────────────────────────────────────────────────────────
prompt = st.chat_input("Escribe tu consulta...")

if prompt:
    # Agregar al historial
    st.session_state.oai_historial.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if MODO_REAL:
            try:
                respuesta = st.write_stream(
                    respuesta_openai_stream(
                        st.session_state.oai_historial,
                        modelo, max_tokens, temperatura
                    )
                )
            except Exception as e:
                st.error(f"❌ Error con OpenAI: {e}")
                respuesta = f"Error: {e}"
        else:
            respuesta = st.write_stream(respuesta_demo_stream(prompt))

    st.session_state.oai_historial.append({"role": "assistant", "content": respuesta})
