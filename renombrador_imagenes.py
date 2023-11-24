import sys
from resources.modules.os_module import select_folder
from resources.modules.image_module import get_images, rename_image, rename_images
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QMessageBox,
    QLineEdit, QHBoxLayout, QWidget, QProgressBar, QLabel,
    QVBoxLayout, QGridLayout
)
from PyQt5.QtGui import QIcon


class RenombrarImagenes(QMainWindow):
    def __init__(self):
        """
        Inicializa la clase RenombrarImagenes.
        """
        super().__init__()
        self.folder_path = None
        self.initUI()

    def initUI(self):
        """
        Configura la interfaz de usuario.
        """
        self.setWindowTitle('Renombrar Imágenes por Lote')
        self.setFixedSize(480, 100)  # Establecer tamaño fijo para la ventana

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Disposición horizontal para botón y campo de texto
        hbox_layout = QHBoxLayout()

        self.btnSeleccionar = QPushButton('Seleccionar Carpeta', self)
        self.btnSeleccionar.setFixedWidth(125)  # Establecer el ancho deseado
        self.btnSeleccionar.clicked.connect(self.run_rename_files_images)
        hbox_layout.addWidget(self.btnSeleccionar)

        self.txtRuta = QLabel(self)
        hbox_layout.addWidget(self.txtRuta)

        layout.addLayout(hbox_layout)

        # Cuadrícula para la barra de progreso debajo de los elementos anteriores
        grid_layout = QGridLayout()
        self.title_bar = QLabel('Ningun Proceso Activo', self)
        grid_layout.addWidget(self.title_bar, 0, 0, 1, 2)

        self.barraProgreso = QProgressBar(self)
        self.barraProgreso.setValue(0)
        self.barraProgreso.setTextVisible(True)
        grid_layout.addWidget(self.barraProgreso, 1, 0, 1, 2)

        layout.addLayout(grid_layout)
        # Asegúrate de proporcionar la ruta correcta al archivo .ico
        icono = QIcon('./resources/icons/iconapp.ico')
        self.setWindowIcon(icono)
        self.update_path_text()

    def run_rename_files_images(self):
        """
        Ejecuta el proceso de renombrado de archivos de imágenes.
        """
        self.folder_path = select_folder()
        self.update_path_text()
        self.update_bartitle_text()
        image_info = get_images(self.folder_path, self.update_progress)
        # rename_images(image_info,"temporal")
        if image_info:
            self.update_bartitle_text(image_info)
            # status = True
            status = rename_image(image_info, self.update_progress)

            if status is True:
                QMessageBox.information(
                    self, 'Completado', 'Imágenes renombradas correctamente')
                # Restablecer el texto de title_bar
                self.title_bar.setText('Ningun Proceso Activo')
                # Restablecer el texto de txtRuta
                self.txtRuta.setText('No se ha seleccionado carpeta')
                self.barraProgreso.reset()  # Establecer la barra de progreso a 0

            else:
                QMessageBox.critical(
                    self, 'Error', f'Error al procesar las imágenes: {str(status)}')
        else:
            QMessageBox.critical(
                self, 'Error', f'Error al leer las imágenes: {str(image_info)}')

    def update_progress(self, value):
        """
        Actualiza el progreso de la barra.

        :param value: Valor para actualizar la barra de progreso.
        """"""
        Actualiza el texto de la ruta.
        """
        self.barraProgreso.setValue(value)

    def update_path_text(self):
        """
        Actualiza el título de la barra.

        :param image_info: Información de la imagen para actualizar el título.
        """
        if self.folder_path:
            self.txtRuta.setText('Carpeta Seleccionada: ' + self.folder_path)
        else:
            self.txtRuta.setText('No se ha seleccionado carpeta')

    def update_bartitle_text(self, image_info=None):
        """
        Actualiza el título de la barra.

        :param image_info: Información de la imagen para actualizar el título.
        """
        if self.folder_path:
            self.title_bar.setText(
                'Leyendo imágenes desde : ' + self.folder_path)
        if image_info:
            self.title_bar.setText('Renombrando imágenes')


def main():
    app = QApplication(sys.argv)
    ventana = RenombrarImagenes()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
