import plotly.express as px
import streamlit as st
import time
import pandas as pd
import time 

import plotly.express as px


df_paises = pd.DataFrame({
    "pais": ["USA", "CHN", "DEU", "BRA"],
    "valor": [100, 85, 62, 45]
})

fig = px.choropleth(
    df_paises,
    locations="pais",
    color="valor",      
    hover_name="valor",
    color_continuous_scale="Reds",
    title="Distribución mundial"
)

fig.update_layout(
     geo=dict(showframe=False,
              bgcolor="rgba(0,0,0,0)"),
 )

st.plotly_chart(fig, use_container_width=True)