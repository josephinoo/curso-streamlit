import streamlit as st
import pandas as pd

st.set_page_config(page_title='Datos de Aranceles', page_icon='📊')
st.title('📊 Tabla de Aranceles')

# Cargar archivo desde el sidebar
with st.sidebar:
    st.header('Datos')
    archivo = st.file_uploader('Sube tariff_rates.csv', type=['csv'])

# Si no hay archivo → mostrar mensaje y detener
if archivo is None:
    st.info('Sube el archivo CSV desde el panel lateral para comenzar.')
    st.stop()

# Cargar datos
df = pd.read_csv(archivo)

# Filtros en el sidebar
with st.sidebar:
    st.subheader('Filtros')
    paises = ['Todos'] + sorted(df['country'].unique().tolist())
    pais = st.selectbox(label='País:',options= paises)
    categorias = ['Todas'] + sorted(df['product_category'].unique().tolist())
    cat = st.selectbox('Categoría:', categorias)


df_f = df.copy()
if pais != 'Todos':
    df_f = df_f[df_f['country'] == pais]
if cat != 'Todas':
    df_f = df_f[df_f['product_category'] == cat]

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric('Registros',df.shape[0],border=True)
col2.metric('Países únicos', df_f['country'].nunique(),border=True)
col3.metric('Arancel máx',   f"{df_f['tariff_rate_pct'].max():.1f}%",border=True)

st.divider()
st.dataframe(df_f)
