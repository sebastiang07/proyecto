from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QWidget

from clases.integracion_inversa import IntegracionInversa


class VentanaIntegracionInversa(QWidget):
    def __init__(self):
        super().__init__()
        ruta_ui = Path(__file__).resolve().parent.parent / "gui" / "ventana_integracion_inversa.ui"
        uic.loadUi(str(ruta_ui), self)
        self.casos = {
            self.pushButtonCaso1: ("0.20", "6"),
            self.pushButtonCaso2: ("0.45", "15"),
            self.pushButtonCaso3: ("0.495", "4"),
        }
        self._conectar_eventos()

    def _conectar_eventos(self):
        self.pushButtonCalcular.clicked.connect(self.calcular)
        for boton, (p, dof) in self.casos.items():
            boton.clicked.connect(lambda _, p_actual=p, dof_actual=dof: self.cargar_caso_prueba(p_actual, dof_actual))

    def cargar_caso_prueba(self, p, dof):
        self.lineEditP.setText(p)
        self.lineEditDof.setText(dof)
        self.lineEditTolerancia.setText("0.00001")

    def calcular(self):
        try:
            p = float(self.lineEditP.text())
            dof = int(self.lineEditDof.text())
            tolerancia = float(self.lineEditTolerancia.text())

            calculadora = IntegracionInversa(p, dof, tolerancia)
            x, p_calculada, error, iteraciones, historial = calculadora.calcular()

            self.labelX.setText(f"{x:.5f}")
            self.labelPCalculada.setText(f"{p_calculada:.5f}")
            self.labelError.setText(f"{error:.8f}")
            self.labelIteraciones.setText(str(iteraciones))
            self._mostrar_historial(historial)

        except ValueError as error:
            self._mostrar_error(str(error))
        except Exception as error:
            self._mostrar_error(f"Ocurrio un error inesperado: {error}")

    def _mostrar_historial(self, historial):
        self.tableWidgetIteraciones.setRowCount(len(historial))

        for fila, dato in enumerate(historial):
            valores = [
                dato["iteracion"],
                f'{dato["x"]:.6f}',
                f'{dato["p_calculada"]:.8f}',
                f'{dato["error_signo"]:.8f}',
                f'{dato["d"]:.6f}',
            ]

            for columna, valor in enumerate(valores):
                self.tableWidgetIteraciones.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def _mostrar_error(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)
