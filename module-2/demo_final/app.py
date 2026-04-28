import streamlit as st

# ⚠️ DEBE ser el PRIMER comando de Streamlit en el archivo
st.set_page_config(
    page_title='Dashboard Aranceles USA',
    page_icon='🇺🇸',

    layout='wide'
)

st.title('🇺🇸 Dashboard — Aranceles USA')
st.write('Bienvenido. Usa el menú lateral para navegar.')
st.info('👈 Selecciona una página en el menú de la izquierda')

st.subheader('Sobre el dataset')
st.write('''
Datos reales de los aranceles anunciados por EE.UU. desde 2018.
Incluye tarifas sobre acero, aluminio, tecnología, bienes de consumo y más.

**Fuente:** Kaggle — US Tariff & Trade War Impact Dataset
''')
