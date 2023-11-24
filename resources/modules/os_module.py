import os
import tkinter as tk
from tkinter import filedialog, messagebox


def select_folder():
    """
    Abre un diálogo para seleccionar una carpeta y devuelve la ruta seleccionada.

    :return: La ruta de la carpeta seleccionada o una cadena vacía si no se selecciona ninguna carpeta.
    """
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    try:
        # Mostrar el diálogo para seleccionar una carpeta
        folder_path = filedialog.askdirectory()

        # Imprimir la ruta de la carpeta seleccionada en la consola
        return folder_path
    except:
        # Si el usuario cancela la selección, mostrar un mensaje y devolver una cadena vacía
        messagebox.showerror("Error", "No se ha seleccionado ninguna carpeta.")
        return ''
