from PyQt6.QtWidgets import QApplication
from view.mainView import MainView


class Simulacion:
    def __init__(self):
        self.app = QApplication([])
        self.main = MainView()
        self.app.exec()
