import os

from PyQt6 import uic


ruta_ui = os.path.join(os.path.dirname(__file__), 'ui/informacion.ui')

class Informacion:
    def __init__(self):
        self.ui = uic.loadUi(ruta_ui)
        self.ui.show()