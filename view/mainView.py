import os

from PyQt6 import uic

from view.acercaDe import AcercaDe
from view.informacion import Informacion
from view.linearRegressionView import LinearRegression

ruta_ui = os.path.join(os.path.dirname(__file__), 'ui/mainView.ui')


class MainView():
    def __init__(self):
        self.ui = uic.loadUi(ruta_ui)
        self.ui.showMaximized()

        self.ui.qa_informacion.triggered.connect(self.openInformacion)
        self.ui.qa_acerca.triggered.connect(self.openAcercaDe)
        self.ui.qa_linear_regression.triggered.connect(self.openLinearRegression)

    def openInformacion(self):
        self.informacion = Informacion()
        return self.informacion

    def openAcercaDe(self):
        self.acerca_de = AcercaDe()
        return self.acerca_de

    def openLinearRegression(self):
        self.linear_regression = LinearRegression()
        return self.linear_regression
