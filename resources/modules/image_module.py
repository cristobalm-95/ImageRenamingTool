import os
from PIL import Image
import re


def get_images(folder, progress_callback=None):
    """
    Obtiene información sobre imágenes dentro de una carpeta.

    :param folder: Ruta de la carpeta a analizar.
    :param progress_callback: Función de devolución de llamada para actualizar el progreso.
    :return: Un diccionario con información de las imágenes encontradas.
    """
    imagenes = {}
    total_files = 0
    processed_files = 0
    for root, subdirs, files in os.walk(folder):
        for archivo in files:
            ruta_archivo = os.path.join(root, archivo)
            if os.path.isfile(ruta_archivo):
                nombre, extension = os.path.splitext(archivo)
                if extension.lower() in ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp', '.ico', '.jfif'):
                    total_files += 1
    try:
        for root, subdirs, files in os.walk(folder):
            for archivo in files:
                processed_files += 1
                ruta_archivo = os.path.join(root, archivo)
                if os.path.isfile(ruta_archivo):
                    nombre, extension = os.path.splitext(archivo)
                    if extension.lower() in ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp', '.ico', '.jfif'):
                        try:
                            with Image.open(ruta_archivo) as imagen:
                                ancho, alto = imagen.size
                            imagen_info = {
                                'nombre': nombre,
                                'extension': extension,
                                'ancho': ancho,
                                'alto': alto,
                                'ubicacion': root,
                                'carpeta': os.path.basename(root)
                            }
                            imagenes[ruta_archivo] = imagen_info
                        except Exception as e:
                            print(
                                f"Error al leer la imagen {ruta_archivo}: {e}")
            if progress_callback is not None:
                progress = int((processed_files / total_files) * 100)
                progress_callback(progress)

        return imagenes
    except Exception as e:
        return e


def rename_image(image_info, progress_callback=None):
    """
    Renombra las imágenes basadas en ciertos criterios de calidad y orientación.

    :param image_info: Información de las imágenes a ser renombradas.
    :param progress_callback: Función de devolución de llamada para actualizar el progreso.
    :return: True si el proceso de renombrado se completa con éxito, de lo contrario, devuelve una excepción.
    """
    try:
        # Definir los umbrales para cada nivel de calidad
        umbral_hq = 172800
        umbral_hd = 921600
        umbral_fullhd = 2073600
        umbral_2k = 2211840
        umbral_4k = 8847360
        total_files = len(image_info)
        processed_files = 0
        # Diccionario para controlar el número de imágenes por carpeta de cada calidad y orientación
        num_imagenes = {
            'LQ': {'Horizontal': {}, 'Vertical': {}, 'Cuadrada': {}},
            'HQ': {'Horizontal': {}, 'Vertical': {}, 'Cuadrada': {}},
            'HD': {'Horizontal': {}, 'Vertical': {}, 'Cuadrada': {}},
            'FullHD': {'Horizontal': {}, 'Vertical': {}, 'Cuadrada': {}},
            '2K': {'Horizontal': {}, 'Vertical': {}, 'Cuadrada': {}},
            '4K': {'Horizontal': {}, 'Vertical': {}, 'Cuadrada': {}}
        }

        for index, (imagen_path, imagen) in enumerate(image_info.items()):

            # Obtener los valores de ancho y alto
            ancho = imagen['ancho']
            alto = imagen['alto']

            # Calcular la resolución de la imagen
            resolucion = ancho * alto
            # Obtener la relación de aspecto de la imagen
            relacion_aspecto = ancho / alto

            # Asignar a cada imagen un nivel de calidad correspondiente
            if resolucion < umbral_hq:
                calidad = 'LQ'
            elif resolucion < umbral_hd:
                calidad = 'HQ'
            elif resolucion < umbral_fullhd:
                calidad = 'HD'
            elif resolucion < umbral_2k:
                calidad = 'FullHD'
            elif resolucion < umbral_4k:
                calidad = '2K'
            else:
                calidad = '4K'

            # Obtener el nombre de la carpeta donde se encuentra la imagen
            carpeta = os.path.basename(imagen['ubicacion'])
            if relacion_aspecto > 1:
                orientacion = 'Horizontal'
            elif relacion_aspecto == 1:
                orientacion = "Cuadrada"
            else:
                orientacion = 'Vertical'

            # Crear el nuevo nombre de la imagen

            nuevo_nombre = f"{orientacion}_{calidad}_{carpeta}"

            if carpeta not in num_imagenes[calidad][orientacion]:
                num_imagenes[calidad][orientacion][carpeta] = 1

            while os.path.exists(os.path.join(imagen['ubicacion'], f"{nuevo_nombre} {num_imagenes[calidad][orientacion][carpeta]}{imagen['extension']}")):
                num_imagenes[calidad][orientacion][carpeta] += 1

            nuevo_nombre = f"{nuevo_nombre} {num_imagenes[calidad][orientacion][carpeta]}{imagen['extension']}"
            # Verificar si el nombre cumple con el formato calidad_nombrecarpeta_orientacion numero.extension

            patron = f"^{orientacion}_{calidad}_{carpeta} [0-9]+$"

            nombre_anterior = imagen["nombre"]
            if not re.match(patron, nombre_anterior):
                # Renombrar la imagen
                nueva_ruta = os.path.join(imagen['ubicacion'], nuevo_nombre)
                os.rename(imagen_path, nueva_ruta)
            processed_files += 1
            if progress_callback is not None:
                progress = int((processed_files / total_files) * 100)
                progress_callback(progress)
        return True
    except Exception as e:
        return e


def rename_images(imagen_info, new_name):
    """
    Renombra las imágenes con un nuevo nombre y un número secuencial.

    :param image_info: Información de las imágenes a ser renombradas.
    :param new_name: Nuevo nombre base para las imágenes.
    """
    count = 1
    for info in imagen_info.values():
        if info['extension'].lower() in ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp', '.ico'):
            new_filename = f'{new_name}_{count}.jpg'
            while os.path.exists(os.path.join(info['ubicacion'], new_filename)):
                count += 1
                new_filename = f'{new_name}_{count}.jpg'
            os.rename(os.path.join(info['ubicacion'], info['nombre'] + info['extension']),
                      os.path.join(info['ubicacion'], new_filename))
            count += 1
