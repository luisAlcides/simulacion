import os

import numpy as np
from sklearn.metrics import r2_score

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout
from PyQt6 import uic
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from utils.util import mostrar_resultado, generar_pdf_dialogo, message
from utils.validation import validate_fields

ruta_ui = os.path.join(os.path.dirname(__file__), 'ui/linearRegressionView.ui')

TABLE_DISTRIBUTION = np.array([[161.4476388, 18.51282051, 10.12796449, 7.70864742,
                                6.60789097, 5.98737761, 5.59144785, 5.31765507,
                                5.11735503, 4.96460274],
                               [199.5, 19., 9.5520945, 6.94427191,
                                5.78613504, 5.14325285, 4.73741413, 4.45897011,
                                4.25649473, 4.10282102],
                               [215.70734537, 19.16429213, 9.27662815, 6.59138212,
                                5.40945132, 4.75706266, 4.3468314, 4.06618055,
                                3.86254836, 3.70826482],
                               [224.58324063, 19.24679434, 9.11718225, 6.38823291,
                                5.19216777, 4.53367695, 4.12031173, 3.83785335,
                                3.63308851, 3.47804969],
                               [230.16187811, 19.29640965, 9.01345517, 6.2560565,
                                5.05032906, 4.38737419, 3.97152315, 3.68749867,
                                3.48165865, 3.32583453],
                               [233.98600036, 19.32953402, 8.94064512, 6.16313228,
                                4.95028807, 4.28386571, 3.86596885, 3.58058032,
                                3.37375365, 3.21717455],
                               [236.76840028, 19.35321754, 8.88674296, 6.09421093,
                                4.8758717, 4.20665849, 3.78704354, 3.50046386,
                                3.29274584, 3.1354648],
                               [238.8826948, 19.3709929, 8.84523846, 6.04104448,
                                4.81831954, 4.14680416, 3.72572532, 3.43810123,
                                3.22958261, 3.07165839],
                               [240.54325471, 19.38482572, 8.81229956, 5.99877903,
                                4.77246561, 4.09901554, 3.6766747, 3.38813023,
                                3.1788931, 3.02038295],
                               [241.88174725, 19.39589672, 8.78552471, 5.96437055,
                                4.73506307, 4.05996279, 3.63652312, 3.34716312,
                                3.13728011, 2.97823702]])


class LinearRegression(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(ruta_ui, self)
        self.showMaximized()

        self.datos_tabla_pdf = []
        self.other_data_pdf = []
        self.other_data2 = []
        self.other_data3 = []
        self.other_data4 = ''

        self.se_calculo = False
        self.ui.btn_calcular.clicked.connect(self.resolver)
        self.ui.btn_limpiar.clicked.connect(self.limpiar)
        self.ui.btn_generar_pdf.clicked.connect(self.generate_pdf)

    def resolver(self):
        try:
            self.datos_tabla_pdf = []
            self.other_data_pdf = []
            self.other_data2 = []
            self.other_data3 = []
            self.other_data4 = ''

            fields = [[self.ui.txt_nombre_empresa_x, 'string', 'nombre empresa x'],
                      [self.ui.txt_x, 'array', 'xi'],
                      [self.ui.txt_nombre_empresa_y, 'string', 'nombre empresa y'],
                      [self.ui.txt_y, 'array', 'yi']]

            if not validate_fields(fields):
                return

            xi_con_comas = self.ui.txt_x.text().strip()
            xi_str = xi_con_comas.split(',')
            xi = [float(number) for number in xi_str]

            yi_con_comas = self.ui.txt_y.text().strip()
            yi_str = yi_con_comas.split(',')
            yi = [float(number) for number in yi_str]

            if len(xi) != len(yi):
                message('Los arreglos deben tener la misma cantidad de elementos')
                return

            n = len(xi)
            xi_sum = sum(xi)
            yi_sum = sum(yi)
            promedio_xi = xi_sum / n
            promedio_yi = yi_sum / n

            xi_menos_promedio_xi = [x - promedio_xi for x in xi]
            yi_menos_promedio_yi = [y - promedio_yi for y in yi]

            xi_menos_promedio_por_yi_menos_promedio = [xi_menos_promedio_xi[i] * yi_menos_promedio_yi[i] for i in
                                                       range(n)]
            sumatoria_varianza = sum(xi_menos_promedio_por_yi_menos_promedio)
            covarianza = np.cov(xi, yi)[0, 1]
            varianza = np.var(xi, ddof=1)

            beta = covarianza / varianza
            des_x = np.std(xi, ddof=1)
            des_y = np.std(yi, ddof=1)
            nivel_correlacion = np.corrcoef(xi, yi)[0, 1]

            # Regresion Lineal
            coeficientes = np.polyfit(xi, yi, deg=1)
            b0 = coeficientes[1]
            b1 = coeficientes[0]

            y_mean = np.mean(yi)

            y_prima = b0 + b1 * np.array(xi)

            # SC
            SCE = np.sum((np.array(yi) - y_prima) ** 2)
            SCR = np.sum((y_prima - y_mean) ** 2)
            SCT = np.sum((np.array(yi) - y_mean) ** 2)

            # R^2
            polinomio = np.poly1d(coeficientes)
            yi_pred = polinomio(xi)
            r2 = r2_score(yi, yi_pred)

            # EMC error medio cuadrado (EMC)
            x_count = len(xi)
            y_count = len(yi)
            k = 1
            n = y_count
            print(n)
            EMC = SCE / (n - k - 1)

            # S
            s = np.sqrt(EMC)

            # Regresion media cuadrada RMC
            RMC = SCR / k

            # Estadisitico F
            F = RMC / EMC

            df1 = k
            df2 = n - k - 1

            df1_index = min(df1 - 1, TABLE_DISTRIBUTION.shape[0] - 1)
            df2_index = min(df2 - 1, TABLE_DISTRIBUTION.shape[1] - 1)

            f_infinito = TABLE_DISTRIBUTION[df1_index, df2_index]
            relation = f'El estadístico F = {F} es mayor que el valor crítico de la tabla F = {f_infinito} Por lo tanto, hay relación'
            no_relation = f'El estadistico F = {F} es menor que el valor critico de la tabla F_infinito={f_infinito} por lo tanto no hay relación'
            if F > f_infinito:
                self.ui.lbl_relation.setText(relation)
                self.other_data4 = relation
            else:
                self.ui.lbl_relation.setText(no_relation)
                self.other_data4 = no_relation

            digito_select = self.ui.cb_digitos.currentText()

            if digito_select == 'Todos':
                digito_select = '50'
            else:
                if digito_select != 'Digitos':
                    digito_select = self.ui.cb_digitos.currentText()
                else:
                    digito_select = '2'

            resultado = [
                [covarianza, "Cov", "Covarianza", False, False, digito_select],
                [varianza, "Var", "Varianza", False, False, digito_select],
                [des_x, "σx", "Desviación estándar x", False, False, digito_select],
                [des_y, "σy", "Desviación estándar y", False, False, digito_select],
                [promedio_xi, "µx", "Promedio x", False, False, digito_select],
                [promedio_yi, "µy", "Promedio y", False, False, digito_select],
                [b0, 'b0', 'Intercepto', False, False, digito_select],
                [b1, 'b1', 'Pendiente', False, False, digito_select],
                [SCR, 'SCR', 'Suma de cuadrados de la regresión', False, False, digito_select],
                [SCE, 'SCE', 'Suma de cuadrados del error', False, False, digito_select],
                [SCT, 'SCT', 'Suma de cuadrados total', False, False, digito_select],
                [r2, 'R^2', 'Coeficiente de determinación', False, True, digito_select],
                [EMC, 'EMC', 'Error medio cuadrado', False, False, digito_select],
                [s, 's', 'Desviación estándar de la regresión', False, False, digito_select],
                [RMC, 'RMC', 'Regresión media cuadrada', False, False, digito_select],
                [F, 'F', 'Estadístico F', False, False, digito_select],
                [(nivel_correlacion * 100), "ρ", "Nivel de correlación", False, True, digito_select],

            ]
            mostrar_resultado(resultado, self.ui.tb_resultado)
            nombre_empresa_x = self.ui.txt_nombre_empresa_x.text().strip()
            nombre_empresa_y = self.ui.txt_nombre_empresa_y.text().strip()
            self.graficar_correlacion(xi, yi, nivel_correlacion, nombre_empresa_x, nombre_empresa_y)

            self.datos_tabla_pdf.append(['Variable', 'Descripción', 'Valor'])
            self.datos_tabla_pdf.append(['Cov', 'Covarianza', covarianza])
            self.datos_tabla_pdf.append(['Var', 'Varianza', varianza])
            self.datos_tabla_pdf.append(['µx', 'Promedio x', promedio_xi])
            self.datos_tabla_pdf.append(['µy', 'Promedio y', promedio_yi])
            self.datos_tabla_pdf.append(['σx', 'Desviación estándar x', des_x])
            self.datos_tabla_pdf.append(['σy', 'Desviación estándar y', des_y])
            self.datos_tabla_pdf.append(['β', 'Beta', beta])

            self.datos_tabla_pdf.append(['ρ', 'Nivel de correlación', nivel_correlacion])
            self.datos_tabla_pdf.append(["Σ", "Sumatoria de (xi - µx)(yi - µy)", sumatoria_varianza])

            self.other_data_pdf.append(['N°', 'xi', 'yi', '(xi - µx)', '(yi - µy)', '(xi - µx)(yi - µy)'])
            for i in range(n):
                self.other_data_pdf.append([i + 1, xi[i], yi[i], xi_menos_promedio_xi[i], yi_menos_promedio_yi[i],
                                            xi_menos_promedio_por_yi_menos_promedio[i]])

            # Linear Regression
            self.other_data2.append(['Variable', 'Descripción', 'Valor'])
            self.other_data2.append(['b0', 'Intercepto', b0])
            self.other_data2.append(['b1', 'Pendiente', b1])
            self.other_data2.append(['SCR', 'Suma de cuadrados de la regresión', SCR])
            self.other_data2.append(['SCE', 'Suma de cuadrados del error', SCE])
            self.other_data2.append(['SCT', 'Suma de cuadrados total', SCT])
            self.other_data2.append(['R^2', 'Coeficiente de determinación', r2])
            self.other_data2.append(['EMC', 'Error medio cuadrado', EMC])
            self.other_data2.append(['s', 'Desviación estándar de la regresión', s])
            self.other_data2.append(['RMC', 'Regresión media cuadrada', RMC])
            self.other_data2.append(['F', 'Estadístico F', F])
            self.other_data2.append(['df1', 'Grados de libertad 1', df1])
            self.other_data2.append(['df2', 'Grados de libertad 2', df2])
            self.other_data2.append(['F_infinito', 'Valor crítico de la tabla F', f_infinito])

            self.other_data3.append(['N°', 'x', 'b1', 'b0', 'y'])
            for i in range(n):
                self.other_data3.append([i + 1, xi[i], b1, b0, b0 + b1 * xi[i]])
            self.se_calculo = True

        except Exception as e:
            message(f'Ha ocurrido un error al realizar el calculo: {e} ')

    def limpiar(self):
        self.ui.txt_x.clear()
        self.ui.txt_y.clear()
        self.ui.tb_resultado.clear()
        self.datos_tabla_pdf = []
        self.other_data_pdf = []
        self.other_data2 = []
        self.other_data3 = []
        self.other_data4 = ''
        self.se_calculo = False
        self.ui.txt_nombre_empresa_x.clear()
        self.ui.txt_nombre_empresa_y.clear()
        self.ui.cb_digitos.setCurrentIndex(0)

        if self.ui.widgetGrafico.layout() is not None:
            while self.ui.widgetGrafico.layout().count():
                child = self.ui.widgetGrafico.layout().takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()

    def graficar_correlacion(self, xi, yi, correlacion, nombre_empresa_x, nombre_empresa_y):
        # Ajuste polinomial
        coeficientes = np.polyfit(xi, yi, 1)
        polinomio = np.poly1d(coeficientes)
        xi_ordenado = np.unique(xi)
        yi_ajuste = polinomio(xi_ordenado)

        # Cálculo de R^2
        yi_pred = polinomio(xi)  # Predicciones para xi
        r2 = r2_score(yi, yi_pred)

        # Texto de la ecuación y R^2
        texto_ecuacion = f'y = {coeficientes[0]:.4f}x + {coeficientes[1]:.4f}\n$R^2 = {r2:.4f}$'

        # Creación del gráfico
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

        # Gráfico de dispersión
        ax.scatter(xi, yi, label='Datos')
        # Línea de mejor ajuste punteada
        ax.plot(xi_ordenado, yi_ajuste, 'r--', label='Mejor ajuste')  # Hacemos la línea punteada con 'r--'
        # Agregar texto de la ecuación y R^2 al gráfico
        ax.text(.40, 0.95, texto_ecuacion, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # Configuraciones del gráfico
        ax.set_title(f'Correlación: {(correlacion * 100):.2f}%')
        ax.set_xlabel(nombre_empresa_x)
        ax.set_ylabel(nombre_empresa_y)
        ax.legend()
        ax.grid(True)
        fig.savefig('correlacion.png')

        # Añadir el gráfico al layout de la interfaz gráfica
        if self.ui.widgetGrafico.layout() is None:
            layout = QVBoxLayout(self.ui.widgetGrafico)
            self.ui.widgetGrafico.setLayout(layout)
        else:
            while self.ui.widgetGrafico.layout().count():
                child = self.ui.widgetGrafico.layout().takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(canvas, self)
        self.ui.widgetGrafico.layout().addWidget(toolbar)
        self.ui.widgetGrafico.layout().addWidget(canvas)

    def generate_pdf(self):
        if self.se_calculo:
            generar_pdf_dialogo('Estadistica', self.datos_tabla_pdf, 'correlacion.png',
                                self.other_data_pdf, 'Regresión Lineal', self.other_data2, self.other_data3,
                                self.other_data4)
        else:
            message('No se ha realizado ningún cálculo')
