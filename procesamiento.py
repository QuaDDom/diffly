import pandas as pd
from io import BytesIO
import streamlit as st
from openpyxl.styles import Border, Side
from openpyxl import Workbook

def cargar_archivo(file):
    """
    Carga un archivo Excel en un DataFrame de Pandas.
    """
    try:
        df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

def comparar_listas_dinamico(plantilla_df, actualizada_df):
    """
    Compara dos DataFrames y detecta cambios detallados en todas las columnas.
    Crea un DataFrame procesado que especifica el valor anterior y el nuevo en columnas separadas.
    """
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
                    
                    # Agregar columnas de valores anteriores y nuevos
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

def descargar_archivo(df_original, df_procesado):
    """
    Crea un archivo Excel con dos hojas:
    1. La lista actualizada original.
    2. La lista procesada con detalles de cambios.
    """
    try:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_original.to_excel(writer, sheet_name="Lista Actualizada", index=False)
            df_procesado.to_excel(writer, sheet_name="Resumen de Cambios", index=False)

            workbook = writer.book
            worksheet = writer.sheets["Resumen de Cambios"]

            # Ajustar el ancho de las columnas automáticamente
            for column_cells in worksheet.columns:
                max_length = max(len(str(cell.value) or "") for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = max_length + 2

            # Aplicar bordes finos a todas las celdas
            thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
            for row in worksheet.iter_rows():
                for cell in row:
                    cell.border = thin_border

        output.seek(0)
        return output
    except Exception as e:
        st.error(f"Error al preparar el archivo para la descarga: {e}")
        return None

def mostrar_resultados_comparacion(cambios, cambios_detallados, plantilla_procesada):
    """
    Muestra el resumen y los detalles de los cambios detectados, incluyendo una vista de la planilla procesada.
    """
    st.subheader("🔍 Resumen Detallado de Cambios Detectados")
    
    # Mostrar resumen de cambios generales por SKU
    st.write("### Cambios Generales por SKU")
    cambios_df = pd.DataFrame(cambios, columns=["SKU", "Estado"])
    st.dataframe(cambios_df)
    
    # Mostrar detalles específicos de cada cambio en columnas separadas
    st.write("### Cambios Detallados por Columna")
    cambios_detallados_df = pd.DataFrame(cambios_detallados)
    st.dataframe(cambios_detallados_df)
    
    # Vista previa del DataFrame procesado con columnas adicionales para valor anterior y valor nuevo
    st.write("### Vista Completa de la Planilla Procesada")
    st.dataframe(plantilla_procesada)
