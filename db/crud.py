# db/crud.py
import pandas as pd
from db.db import get_connection
import streamlit as st

def insertar_comparacion(fecha, nombre_archivo_ref, nombre_archivo_act, resultado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO comparaciones (fecha, nombre_archivo_ref, nombre_archivo_act, resultado) VALUES (?, ?, ?, ?)
    """, (fecha, nombre_archivo_ref, nombre_archivo_act, resultado))
    conn.commit()
    conn.close()
    
    # Incrementar el contador de actualización en session_state
    if "update_counter" in st.session_state:
        st.session_state.update_counter += 1

def obtener_comparaciones():
    conn = get_connection()
    comparaciones = pd.read_sql_query("SELECT id, fecha, nombre_archivo_ref, nombre_archivo_act FROM comparaciones", conn)
    conn.close()
    return comparaciones

def eliminar_comparacion(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comparaciones WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    # Incrementar el contador de actualización en session_state
    if "update_counter" in st.session_state:
        st.session_state.update_counter += 1

def obtener_resultado_comparacion(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT resultado FROM comparaciones WHERE id = ?", (id,))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado
