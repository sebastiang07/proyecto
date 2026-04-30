from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QWidget

from clases.rango_prediccion import RangoPrediccion


class CasoRango:
    def __init__(self, x, y, xk):
        self.x = x
        self.y = y
        self.xk = xk

    def cargar(self, ventana):
        ventana.cargar_datos(self.x, self.y)
        ventana.lineEditXK.setText(str(self.xk))


class VentanaRango(QWidget):
    def __init__(self):
        super().__init__()
        ruta_ui = Path(__file__).resolve().parent.parent / "gui" / "ventana_rango.ui"
        uic.loadUi(str(ruta_ui), self)
        self.casos = self._crear_casos()
        self._conectar_eventos()

    def _crear_casos(self):
        return {
            self.pushButtonCaso1: CasoRango(
                [130, 650, 99, 150, 128, 302, 95, 945, 368, 961],
                [186, 699, 132, 272, 291, 331, 199, 1890, 788, 1601],
                386,
            ),
            self.pushButtonCaso2: CasoRango(
                [130, 650, 99, 150, 128, 302, 95, 945, 368, 961],
                [15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2],
                386,
            ),
        }

    def _conectar_eventos(self):
        self.pushButtonCalcular.clicked.connect(self.calcular)
        for boton, caso in self.casos.items():
            boton.clicked.connect(lambda _, caso_actual=caso: self.cargar_caso_prueba(caso_actual))

    def cargar_caso_prueba(self, caso):
        caso.cargar(self)
        self.lineEditP.setText("0.35")
        self.lineEditTolerancia.setText("0.00001")

    def cargar_datos(self, x, y):
        self.tableWidgetDatos.setRowCount(len(x))
        for fila, (valor_x, valor_y) in enumerate(zip(x, y)):
            self.tableWidgetDatos.setItem(fila, 0, QTableWidgetItem(str(valor_x)))
            self.tableWidgetDatos.setItem(fila, 1, QTableWidgetItem(str(valor_y)))

    def leer_datos(self):
        x = []
        y = []

        for fila in range(self.tableWidgetDatos.rowCount()):
            item_x = self.tableWidgetDatos.item(fila, 0)
            item_y = self.tableWidgetDatos.item(fila, 1)

            if item_x and item_y and item_x.text().strip() and item_y.text().strip():
                x.append(float(item_x.text()))
                y.append(float(item_y.text()))

        return x, y

    def calcular(self):
        try:
            x, y = self.leer_datos()
            xk = float(self.lineEditXK.text())
            p = float(self.lineEditP.text())
            tolerancia = float(self.lineEditTolerancia.text())

            resultado = RangoPrediccion(x, y, xk, p, tolerancia).calcular()
            self._mostrar_resultados(resultado)

        except ValueError as error:
            self._mostrar_error(str(error))
        except Exception as error:
            self._mostrar_error(f"Ocurrio un error inesperado: {error}")

    def _mostrar_resultados(self, resultado):
        self.labelR2.setText(f'{resultado["r2"]:.4f}')
        self.labelB0.setText(f'{resultado["b0"]:.4f}')
        self.labelB1.setText(f'{resultado["b1"]:.4f}')
        self.labelYk.setText(f'{resultado["yk"]:.4f}')
        self.labelT.setText(f'{resultado["t"]:.5f}')
        self.labelSigma.setText(f'{resultado["sigma"]:.4f}')
        self.labelRango.setText(f'{resultado["rango"]:.4f}')
        self.labelUPI.setText(f'{resultado["upi"]:.4f}')
        self.labelLPI.setText(f'{resultado["lpi"]:.4f}')
        self.labelSignificancia.setText(f'{resultado["significancia"]:.2f}')

    def _mostrar_error(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)
