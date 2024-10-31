import streamlit as st
import plotly.express as px
import pandas as pd 

def visualizar_cambios(cambios):
    """
    Genera un gráfico de pastel para visualizar los tipos de cambios detectados.
    """
    # Convertir la lista de cambios en un DataFrame
    cambios_df = pd.DataFrame(cambios, columns=["SKU", "Estado"])
    
    # Contar los tipos de cambios y crear el gráfico de pastel
    conteo_cambios = cambios_df['Estado'].value_counts().reset_index()
    conteo_cambios.columns = ["Estado", "Cantidad"]
    
    fig = px.pie(conteo_cambios, names='Estado', values='Cantidad', title="Distribución de Cambios")
    st.plotly_chart(fig, use_container_width=True)
