import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Gráficos de Aranceles', page_icon='📈')

st.title('📈 Gráfico de Aranceles')

with st.sidebar:
    st.header('Datos')
    archivo = st.file_uploader('Sube tariff_rates.csv', type=['csv'])

if archivo is None:
    st.info('Sube el archivo CSV desde el panel lateral para comenzar.')
    st.stop()


df = pd.read_csv(archivo)

with st.sidebar:
    st.divider()
    tipo = st.radio(label='Tipo de gráfico:', options=['Por país', 'Por fecha', 'Por categoría'])

if tipo == 'Por país':
    resumen = df.groupby('country')['tariff_rate_pct'].mean().reset_index()
    fig = px.bar(resumen.sort_values('tariff_rate_pct'),
        x='tariff_rate_pct', y='country', orientation='h',
        title='Arancel promedio por país',
        color='tariff_rate_pct', color_continuous_scale='Reds',
        labels={'tariff_rate_pct': 'Arancel (%)', 'country': 'País'})

elif tipo == 'Por fecha':
    fig = px.scatter(df, x='date', y='tariff_rate_pct', color='country',
        title='Anuncios de aranceles en el tiempo',
        labels={'date': 'Fecha', 'tariff_rate_pct': 'Arancel (%)', 'country': 'País'})

elif tipo == 'Por categoría':
    fig = px.pie(df, names='product_category', values='tariff_rate_pct',
        title='Distribución de aranceles por categoría de producto')

st.plotly_chart(fig)

# Tabla debajo del gráfico
with st.expander('Ver datos del gráfico'):
    st.dataframe(df,
        use_container_width=True, height=200)

