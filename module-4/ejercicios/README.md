# 📚 Módulo 4 — Archivos de Práctica

## Estructura

```
modulo4/
│
├── bloque1_formularios/
│   ├── 01_problema_reruns.py     ← Ver el problema sin st.form
│   ├── 02_form_basico.py         ← st.form resuelve el problema
│   └── 03_form_avanzado.py       ← Validación + cache_data
│
├── bloque2_seguridad/
│   ├── 01_login_manual.py        ← session_state + st.stop()
│   ├── 02_streamlit_authenticator.py  ← Multi-usuario con stauth
│   └── 03_roles_rbac.py          ← Control de acceso por roles
│
├── bloque3_fragmentos/
│   ├── 01_fragment_basico.py     ← @st.fragment, ciclo de vida
│   ├── 02_fragment_run_every.py  ← Live dashboard auto-actualizable
│   └── 03_multi_fragment.py      ← Múltiples fragmentos independientes
│
├── bloque4_chat/
│   ├── 01_chat_basico.py         ← Chat con historial + write_stream
│   └── 02_chat_openai.py         ← Conexión real a OpenAI (opcional)
│
└── app_completa/
    └── app_completa.py           ← Integración de todos los bloques
```

## Instalación

```bash
pip install streamlit pandas numpy plotly streamlit-authenticator
pip install openai   # solo para ejercicio 02_chat_openai.py
```

## Cómo correr cada ejercicio

```bash
# Bloque 1
streamlit run bloque1_formularios/01_problema_reruns.py
streamlit run bloque1_formularios/02_form_basico.py
streamlit run bloque1_formularios/03_form_avanzado.py

# Bloque 2
streamlit run bloque2_seguridad/01_login_manual.py
streamlit run bloque2_seguridad/02_streamlit_authenticator.py
streamlit run bloque2_seguridad/03_roles_rbac.py

# Bloque 3
streamlit run bloque3_fragmentos/01_fragment_basico.py
streamlit run bloque3_fragmentos/02_fragment_run_every.py
streamlit run bloque3_fragmentos/03_multi_fragment.py

# Bloque 4
streamlit run bloque4_chat/01_chat_basico.py
streamlit run bloque4_chat/02_chat_openai.py

# App completa
streamlit run app_completa/app_completa.py
```

## Credenciales para los ejercicios de login

| Usuario | Contraseña | Rol    |
|---------|-----------|--------|
| admin   | clave123  | -      |
| ana     | pass123   | admin  |
| carlos  | pass456   | viewer |

## secrets.toml (opcional, para ejercicios de seguridad)

Crear `.streamlit/secrets.toml` en la raíz del proyecto:

```toml
USUARIO_ADMIN = "admin"
CLAVE_ADMIN   = "clave123"
JWT_SECRET    = "clave_firma_muy_secreta_2026"

# Solo para 02_chat_openai.py
OPENAI_KEY = "sk-proj-tu-clave-aqui"
```

## Orden sugerido para la clase

1. `01_problema_reruns.py` → mostrar el problema
2. `02_form_basico.py` → mostrar la solución
3. `01_login_manual.py` → introducir seguridad
4. `02_streamlit_authenticator.py` → login profesional
5. `01_fragment_basico.py` → concepto de fragmento
6. `02_fragment_run_every.py` → live data
7. `01_chat_basico.py` → UI de chat
8. `app_completa.py` → todo integrado
