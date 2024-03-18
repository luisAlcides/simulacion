import os

from PyQt6 import uic

ruta_ui = os.path.join(os.path.dirname(__file__), 'ui/acercaDe.ui')

class AcercaDe:
    def __init__(self):
        self.ui = uic.loadUi(ruta_ui)
        self.ui.show()