import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 

def visualizar_cambios(cambios):
    """
    Genera gráficos para visualizar los tipos de cambios detectados.
    """
    # Convertir la lista de cambios en un DataFrame
    cambios_df = pd.DataFrame(cambios, columns=["SKU", "Estado"])
    
    # Contar los tipos de cambios y crear un gráfico de pastel
    conteo_cambios = cambios_df['Estado'].value_counts().reset_index()
    conteo_cambios.columns = ["Estado", "Cantidad"]
    
    fig_pie = px.pie(conteo_cambios, names='Estado', values='Cantidad', title="Distribución de Cambios", hole=0.4)
    fig_pie.update_traces(textinfo='percent+label')

    # Crear un gráfico de barras para visualizar los tipos de cambios
    fig_bar = go.Figure(go.Bar(
        x=conteo_cambios['Estado'],
        y=conteo_cambios['Cantidad'],
        text=conteo_cambios['Cantidad'],
        textposition='auto'
    ))
    fig_bar.update_layout(
        title="Conteo de Cambios por Estado",
        xaxis_title="Estado",
        yaxis_title="Cantidad",
        template="plotly_white"
    )

    # Mostrar ambos gráficos
    st.plotly_chart(fig_pie, use_container_width=True)
    st.plotly_chart(fig_bar, use_container_width=True)
