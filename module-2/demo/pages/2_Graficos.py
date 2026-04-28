import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gráficos cambios ejemplo", page_icon="📈")

st.title("📈 Gráfico de Aranceles")
archivo = st.sidebar.file_uploader("Sube el CSV", type=["csv"])

if archivo is None:
    st.info("Sube el archivo CSV desde el panel lateral.")
    st.stop()           # ← para aquí si no hay archivo

df = pd.read_csv(archivo)
resumen = df.groupby("country")["tariff_rate_pct"].mean().reset_index()

fig = px.bar(resumen.sort_values("tariff_rate_pct"),
    x="country", y="tariff_rate_pct",orientation="v",
    title="Arancel promedio por país",
    color="tariff_rate_pct", color_continuous_scale="Reds",
    labels={"tariff_rate_pct": "Arancel (%)", "country": "País"})
st.plotly_chart(fig, use_container_width=True)