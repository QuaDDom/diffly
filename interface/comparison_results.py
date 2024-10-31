import streamlit as st
import pandas as pd

def mostrar_resultados_comparacion(cambios, cambios_detallados, plantilla_procesada):
    """
    Muestra el resumen y los detalles de los cambios detectados, incluyendo una vista de la planilla procesada.
    """
    st.subheader("🔍 Resumen Detallado de Cambios Detectados")
    
    # Mostrar resumen de cambios generales por SKU
    st.write("### Cambios Generales por SKU")
    cambios_df = pd.DataFrame(cambios, columns=["SKU", "Estado"])
    st.dataframe(cambios_df, use_container_width=True)
    
    # Mostrar detalles específicos de cada cambio en columnas separadas
    st.write("### Cambios Detallados por Columna")
    cambios_detallados_df = pd.DataFrame(cambios_detallados)
    st.dataframe(cambios_detallados_df, use_container_width=True)
    
    # Vista previa del DataFrame procesado con columnas adicionales para valor anterior y valor nuevo
    st.write("### Vista Completa de la Planilla Procesada")
    st.dataframe(plantilla_procesada, use_container_width=True)
