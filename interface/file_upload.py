# interface/cargar_archivo.py

import streamlit as st
import pandas as pd

def cargar_archivo(file):
    """
    Carga un archivo Excel en un DataFrame de Pandas.
    
    Parámetros:
        file: Archivo subido por el usuario.
        
    Retorna:
        DataFrame con los datos del archivo, o None si ocurre un error.
    """
    try:
        df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None
