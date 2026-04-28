import plotly.express as px

import pandas as pd

# Necesitas códigos ISO alpha-3
df_paises = pd.DataFrame({
    "pais": ["USA", "CHN", "DEU", "BRA"],
    "valor": [100, 85, 62, 45]
})

fig = px.choropleth(
    df_paises,
    locations="pais",   # columna con código ISO
    color="valor",      # columna a visualizar
    hover_name="pais",
    color_continuous_scale="Reds",
    title="Distribución mundial"
)

fig.update_layout(
    geo=dict(showframe=False,
             bgcolor="rgba(0,0,0,0)"),
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#e8e8e8"
)

st.plotly_chart(fig, use_container_width=True)