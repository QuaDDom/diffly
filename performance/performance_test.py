import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Diccionario global para almacenar los tiempos de ejecución
tiempos_registro = {}

# Función para monitorear el tiempo de ejecución
def medir_tiempo_ejecucion(funcion, nombre_funcion, *args, **kwargs):
    start_time = time.time()
    resultado = funcion(*args, **kwargs)
    end_time = time.time()
    tiempo_ejecucion = end_time - start_time
    
    # Guardar el tiempo en el registro global
    if nombre_funcion not in tiempos_registro:
        tiempos_registro[nombre_funcion] = []
    tiempos_registro[nombre_funcion].append(tiempo_ejecucion)
    
    return resultado, tiempo_ejecucion

# Función para mostrar los datos de rendimiento en texto y gráficos mejorados
def mostrar_datos_rendimiento(tiempos):
    st.markdown("## 📊 Desempeño de Ejecución", unsafe_allow_html=True)
    
    if tiempos:
        # Mostrar una tabla de resumen con la última ejecución y el promedio
        ultimos_tiempos = {funcion: tiempos[-1] for funcion, tiempos in tiempos_registro.items()}
        promedios_tiempos = {funcion: sum(tiempos)/len(tiempos) for funcion, tiempos in tiempos_registro.items()}
        
        resumen_df = pd.DataFrame({
            "Función": ultimos_tiempos.keys(),
            "Última Ejecución (s)": ultimos_tiempos.values(),
            "Promedio (s)": promedios_tiempos.values()
        })
        st.table(resumen_df.style.format({"Última Ejecución (s)": "{:.2f}", "Promedio (s)": "{:.2f}"}).set_caption("Resumen de tiempos de ejecución").set_table_styles(
            [{"selector": "caption", "props": [("font-size", "18px"), ("font-weight", "bold"), ("color", "#4CAF50")]}]
        ))

        # Convertir el registro en un DataFrame para visualización
        registros_df = pd.DataFrame(tiempos_registro)

        # Gráfico de líneas para mostrar la evolución del tiempo de cada función
        fig_line = px.line(
            registros_df, 
            markers=True, 
            title="⏱ Evolución del Tiempo de Ejecución por Función",
            labels={"index": "Ejecuciones", "value": "Tiempo (segundos)", "variable": "Función"}
        )
        fig_line.update_layout(
            title_x=0.5, 
            xaxis=dict(showgrid=True, gridcolor="LightGray"),
            yaxis=dict(showgrid=True, gridcolor="LightGray"),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        fig_line.update_traces(marker=dict(size=8, line=dict(width=2, color="DarkSlateGray")))
        st.plotly_chart(fig_line, use_container_width=True)

        # Gráfico de barras de la última ejecución para comparación
        fig_bar = go.Figure(data=[
            go.Bar(name=funcion, x=[funcion], y=[tiempo], text=f"{tiempo:.2f} s", textposition="outside")
            for funcion, tiempo in ultimos_tiempos.items()
        ])
        fig_bar.update_layout(
            title="📉 Comparación de Tiempos en la Última Ejecución",
            xaxis_title="Función",
            yaxis_title="Tiempo (segundos)",
            title_x=0.5,
            template="plotly_white",
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40),
            yaxis=dict(showgrid=True, gridcolor="LightGray"),
            xaxis=dict(showgrid=False)
        )
        fig_bar.update_traces(marker_color="LightSeaGreen", marker_line_color="DarkSlateGray", marker_line_width=1.5)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.write("No hay datos de rendimiento disponibles. Realiza una ejecución para visualizar el rendimiento.")
