from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QWidget

from clases.simpson import Simpson


class VentanaBase(QWidget):
    def __init__(self, ui_filename):
        super().__init__()

        ui_path = Path(__file__).resolve().parent.parent / "gui" / ui_filename
        uic.loadUi(str(ui_path), self)

        self.configurar_eventos()

    def configurar_eventos(self):
        """
        Método que las clases hijas deben sobrescribir
        """
        pass


class VentanaEjercicio2(VentanaBase):
    def __init__(self):
        super().__init__("ventana_simpson.ui")

    def configurar_eventos(self):
        self.pushButtonCalcular.clicked.connect(self.calcular_probabilidad)

    def calcular_probabilidad(self):
        try:
            x = float(self.lineEditX.text())
            dof = int(self.lineEditDof.text())
            num_seg = int(self.lineEditNumSeg.text())
            error = float(self.lineEditError.text())

            if x <= 0:
                raise ValueError("X debe ser mayor que cero.")
            if dof <= 0:
                raise ValueError("Los grados de libertad deben ser mayores que cero.")
            if num_seg <= 0 or num_seg % 2 != 0:
                raise ValueError("Los segmentos iniciales deben ser un numero par y positivo.")
            if error <= 0:
                raise ValueError("El error aceptable debe ser mayor que cero.")

            integrador = Simpson(x, dof, num_seg, error)
            resultado, segmentos_finales = integrador.integrar()

            self.labelResultado.setText(f"{resultado:.5f}")
            self.labelSegmentos.setText(str(segmentos_finales))

        except ValueError as error_validacion:
            self.mostrar_error(str(error_validacion))
        except Exception as error_inesperado:
            self.mostrar_error(f"Ocurrio un error inesperado: {error_inesperado}")

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)


class VentanaSimpson(VentanaEjercicio2):
    pass
