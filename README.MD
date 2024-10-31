# Diffly 📊

Diffly es una aplicación diseñada para simplificar y automatizar la comparación de tablas de Excel. Ideal para rastrear cambios, actualizaciones y modificaciones en diversas tablas de datos, Diffly es flexible y se adapta a múltiples casos de uso, desde la gestión de inventarios hasta necesidades más generales de comparación de datos.

## Contenido

- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## Características

- **Comparación Automática de Datos**: Sube dos archivos de Excel para detectar y visualizar rápidamente las diferencias entre ellos.
- **Seguimiento Detallado de Cambios**: Visualiza modificaciones específicas a nivel de columna, identificando tanto los valores anteriores como los nuevos.
- **Análisis Visual**: Genera gráficos de pastel para analizar visualmente el tipo y la distribución de los cambios.
- **Gestión de Historial**: Guarda y administra un historial de comparaciones para futuras referencias.
- **Exportación de Datos**: Descarga los resultados de la comparación en un archivo de Excel procesado.

## Instalación

### Requisitos Previos

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Pasos

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/diffly.git
   cd diffly
   ```

2. Instala las dependencias requeridas:

   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:

   ```bash
   streamlit run main.py
   ```

## Uso

1. **Subir Archivos**: En la barra lateral, sube los archivos de Excel de referencia y el archivo actualizado que deseas comparar.
2. **Ver Diferencias**: Haz clic en "Comparar Archivos" para generar una comparación detallada, que incluye resúmenes visuales y cambios específicos por columna.
3. **Gestionar Historial**: Accede a las comparaciones guardadas, visualiza los detalles y descarga los resultados anteriores.
4. **Eliminar Comparaciones**: Elimina comparaciones antiguas del historial cuando sea necesario.

## Estructura del Proyecto

```
diffly/
├── db/
│   ├── crud.py                # Operaciones CRUD para la gestión de la base de datos
│   ├── db.py                  # Inicialización de la base de datos
├── interface/
│   ├── chart_visualization.py # Funciones de visualización de gráficos
│   ├── comparison_results.py  # Interfaz para mostrar resultados de comparación
│   ├── file_upload.py         # Funciones para la carga y procesamiento de archivos
├── main.py                    # Script principal de la aplicación
├── procesamiento.py           # Lógica principal de procesamiento y comparación
├── comparaciones.db           # Base de datos SQLite para almacenar el historial
├── README.md                  # Documentación del proyecto
└── requirements.txt           # Dependencias de Python
```

## Capturas de Pantalla

### Subir y Comparar

*Sube tus archivos de referencia y actualizados para una comparación rápida.*

![Captura de Pantalla de Subida](link_a_captura_subida.png)

### Visualizar Cambios

*Visualiza un resumen de los cambios con gráficos.*

![Captura de Pantalla de Visualización](link_a_captura_visualizacion.png)

### Gestionar Historial

*Accede a comparaciones previas y descarga los resultados.*

![Captura de Pantalla del Historial](link_a_captura_historial.png)

> **Nota**: Reemplaza los enlaces de las imágenes anteriores con enlaces reales o rutas a las capturas de pantalla en el repositorio.

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, abre un issue o crea un pull request con tus cambios.

1. Haz un fork del proyecto.
2. Crea tu rama de funcionalidad: `git checkout -b feature/TuFuncionalidad`
3. Realiza tus cambios: `git commit -m 'Agrega TuFuncionalidad'`
4. Haz push a la rama: `git push origin feature/TuFuncionalidad`
5. Abre un pull request.

## Licencia

Distribuido bajo la Licencia MIT. Consulta el archivo `LICENSE` para más información.

---

Con **Diffly**, la comparación de datos en Excel es más fácil que nunca, ya sea para la gestión de inventarios o auditorías de datos en general. ¡Disfruta del seguimiento y la gestión de cambios con solo unos clics!

---
