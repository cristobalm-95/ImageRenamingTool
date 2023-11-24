# Renombrador de Imágenes por Lote

Este programa en Python proporciona una interfaz gráfica para renombrar imágenes en lotes según ciertos criterios de calidad, orientación y resolución.

## Características

- **Selección de Carpeta**: Permite al usuario seleccionar una carpeta que contiene las imágenes a ser renombradas.
- **Análisis de Imágenes**: Escanea la carpeta seleccionada para identificar las imágenes y recopilar información relevante, como resolución, orientación, calidad, etc.
- **Renombrado Automático**: Basándose en la calidad, orientación y resolución de cada imagen, las renombra siguiendo un formato predefinido.
- **Interfaz Gráfica**: Ofrece una interfaz de usuario intuitiva y sencilla para realizar estas operaciones.
  
## Requisitos

- Python 3.x
- Bibliotecas: `os`, `tkinter`, `PIL`, `re`

## Uso

1. **Ejecución**: Ejecutar el programa `renombrador_imagenes.py`.
2. **Seleccionar Carpeta**: Hacer clic en "Seleccionar Carpeta" y elegir la carpeta que contiene las imágenes a renombrar.
3. **Proceso de Renombrado**: El programa analizará las imágenes y las renombrará automáticamente.
4. **Resultados**: Se mostrará un mensaje indicando si el proceso se completó con éxito o si hubo errores.
  
## Funciones Principales

- `get_images(folder, progress_callback=None)`: Obtiene información sobre las imágenes dentro de una carpeta.
- `rename_image(image_info, progress_callback=None)`: Renombra las imágenes basándose en ciertos criterios de calidad y orientación.
- `rename_images(image_info, new_name)`: Renombra las imágenes con un nuevo nombre y un número secuencial.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, puedes hacer un fork del repositorio, realizar cambios y enviar un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

---

¡Gracias por utilizar el Renombrador de Imágenes por Lote! Si tienes sugerencias, problemas o mejoras, no dudes en comunicarte.
