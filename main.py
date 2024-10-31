import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from streamlit.components.v1 import html

from db.db import init_db
from db.crud import insertar_comparacion, obtener_comparaciones, eliminar_comparacion, obtener_resultado_comparacion
from interface.chart_visualization import visualizar_cambios
from interface.comparison_results import mostrar_resultados_comparacion
from interface.file_upload import cargar_archivo

# Configuración de la base de datos
st.set_page_config(page_title="Diffly", page_icon="📊", layout="wide")
init_db()

# Inicializar contador de recarga en session_state
if "reload_count" not in st.session_state:
    st.session_state.reload_count = 0

# Función para convertir DataFrame en BytesIO para almacenamiento en la DB
def convertir_a_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output.read()

# Función para comparar listas y detectar cambios
def comparar_listas_dinamico(plantilla_df, actualizada_df):
    plantilla_procesada = plantilla_df.copy()
    plantilla_procesada["Estado"] = "Sin cambios"
    plantilla_procesada["Detalles de Cambios"] = ""
    
    cambios = []
    cambios_detallados = []

    clave_identificacion = plantilla_df.columns[0]
    plantilla_dict = plantilla_df.set_index(clave_identificacion).to_dict("index")
    
    for _, row_actualizada in actualizada_df.iterrows():
        id_valor = row_actualizada[clave_identificacion]
        
        if id_valor in plantilla_dict:
            fila_original = plantilla_dict[id_valor]
            cambios_en_fila = False
            detalles_cambios = []

            for columna in plantilla_df.columns:
                valor_anterior = fila_original.get(columna, None)
                valor_nuevo = row_actualizada[columna]
                
                if pd.notnull(valor_anterior) and pd.notnull(valor_nuevo) and valor_anterior != valor_nuevo:
                    cambios_en_fila = True
                    detalles_cambios.append(f"{columna}: {valor_anterior} -> {valor_nuevo}")
                    
                    plantilla_procesada.loc[plantilla_procesada[clave_identificacion] == id_valor, f"{columna} (Valor Anterior)"] = valor_anterior
                    plantilla_procesada.loc[plantilla_procesada[clave_identificacion] == id_valor, f"{columna} (Valor Nuevo)"] = valor_nuevo
                    cambios_detallados.append({
                        "SKU": id_valor,
                        "Columna": columna,
                        "Valor Anterior": valor_anterior,
                        "Valor Nuevo": valor_nuevo
                    })
            
            if cambios_en_fila:
                plantilla_procesada.loc[plantilla_procesada[clave_identificacion] == id_valor, "Estado"] = "Actualizado"
                plantilla_procesada.loc[plantilla_procesada[clave_identificacion] == id_valor, "Detalles de Cambios"] = "; ".join(detalles_cambios)
                cambios.append((id_valor, "Actualizado"))
            else:
                cambios.append((id_valor, "Sin cambios"))
        else:
            nueva_fila = row_actualizada.to_dict()
            nueva_fila["Estado"] = "Nuevo"
            nueva_fila["Detalles de Cambios"] = "Nuevo registro"
            
            for columna in plantilla_df.columns:
                nueva_fila[f"{columna} (Valor Anterior)"] = None
                nueva_fila[f"{columna} (Valor Nuevo)"] = nueva_fila[columna]
            
            plantilla_procesada = pd.concat([plantilla_procesada, pd.DataFrame([nueva_fila])], ignore_index=True)
            cambios.append((id_valor, "Nuevo"))
            cambios_detallados.append({
                "SKU": id_valor,
                "Columna": "Nuevo registro",
                "Valor Anterior": None,
                "Valor Nuevo": "Nuevo registro"
            })
    
    columnas_finales = [col for col in plantilla_procesada.columns if "(Valor Anterior)" in col or "(Valor Nuevo)" in col or col in [clave_identificacion, "Estado", "Detalles de Cambios"]]
    plantilla_procesada = plantilla_procesada[columnas_finales]
    
    return plantilla_procesada, cambios, cambios_detallados

# Función principal
def main():
    st.title("📊 Diffly")
    st.subheader("Detecta automáticamente cambios en inventarios o listas de proveedores utilizando archivos de Excel.")

    # Panel lateral para historial
    with st.sidebar:
        st.header("📜 Historial de Comparaciones")
        
        # Recargar historial si reload_count cambia
        comparaciones = obtener_comparaciones()
        st.dataframe(comparaciones, use_container_width=True)
        
        if not comparaciones.empty:
            id_seleccionado = st.selectbox("Selecciona una comparación por ID:", comparaciones["id"], key="comparacion_select")
            
            if st.button("Ver Resultado"):
                try:
                    resultado_bytes = obtener_resultado_comparacion(id_seleccionado)
                    resultado_df = pd.read_excel(BytesIO(resultado_bytes))
                    st.write("### Resultado de la Comparación Seleccionada")
                    st.dataframe(resultado_df)
                    
                    st.download_button(
                        label="📅 Descargar Resultado",
                        data=resultado_bytes,
                        file_name=f"resultado_comparacion_{id_seleccionado}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception as e:
                    st.error(f"Error al cargar el resultado de la comparación: {e}")
            
            # Usar st.dialog para confirmación de eliminación
            @st.dialog("Confirmar Eliminación", width="small")
            def eliminar_dialog():
                st.write("¿Estás seguro de que deseas eliminar esta comparación? Esta acción no se puede deshacer.")
                if st.button("Confirmar Eliminación"):
                    try:
                        eliminar_comparacion(id_seleccionado)
                        st.session_state.reload_count += 1  # Incrementar contador para recarga
                        st.success("Comparación eliminada exitosamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al eliminar la comparación: {e}")

            if st.button("Eliminar Comparación"):
                eliminar_dialog()

    # Cargar Archivos y Comparar
    st.write("### Cargar y Comparar Archivos")
    plantilla_file = st.file_uploader("Archivo de referencia (plantilla)", type=["xls", "xlsx"])
    actualizada_file = st.file_uploader("Archivo actualizado", type=["xls", "xlsx"])

    if plantilla_file and actualizada_file:
        plantilla_df = cargar_archivo(plantilla_file)
        actualizada_df = cargar_archivo(actualizada_file)

        if plantilla_df is not None and actualizada_df is not None:
            st.write("### Vista previa de Archivos")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Archivo de Referencia:**")
                st.dataframe(plantilla_df.head())
            with col2:
                st.write("**Archivo Actualizado:**")
                st.dataframe(actualizada_df.head())

            if st.button("Comparar Archivos"):
                with st.spinner("🔍 Comparando archivos..."):
                    try:
                        plantilla_procesada, cambios, cambios_detallados = comparar_listas_dinamico(plantilla_df, actualizada_df)
                        
                        # Mostrar resultados
                        mostrar_resultados_comparacion(cambios, cambios_detallados, plantilla_procesada)
                        visualizar_cambios(cambios)

                        # Guardar en la base de datos
                        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        resultado_bytes = convertir_a_bytes(plantilla_procesada)
                        insertar_comparacion(fecha, plantilla_file.name, actualizada_file.name, resultado_bytes)
                        
                        st.success("Resultados guardados en la base de datos.")
                        st.session_state.reload_count += 1  # Incrementar contador para recarga

                        # Botón para descargar el resultado de la comparación reciente
                        st.download_button(
                            label="📅 Descargar Comparación Reciente",
                            data=resultado_bytes,
                            file_name=f"comparacion_{fecha}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    except Exception as e:
                        st.error(f"Error al comparar los archivos: {e}")

if __name__ == "__main__":
    main()