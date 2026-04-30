import sys
from pathlib import Path

RUTA_EJERCICIO1 = Path(__file__).resolve().parent.parent
if str(RUTA_EJERCICIO1) not in sys.path:
    sys.path.insert(0, str(RUTA_EJERCICIO1))

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem

from clases.regresion import RegresionLineal


class CasoRegresion:
    def obtener_datos(self):
        raise NotImplementedError("La subclase debe definir los datos del caso.")

    def cargar_en_tabla(self, ventana):
        x, y, xk = self.obtener_datos()
        ventana.cargar_datos(x, y)
        ventana.cargar_xk(xk)


class Caso1Regresion(CasoRegresion):
    def obtener_datos(self):
        return (
            [130, 650, 99, 150, 128, 302, 95, 945, 368, 961],
            [186, 699, 132, 272, 291, 331, 199, 1890, 788, 1601],
            386,
        )


class Caso2Regresion(CasoRegresion):
    def obtener_datos(self):
        return (
            [130, 650, 99, 150, 128, 302, 95, 945, 368, 961],
            [15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2],
            386,
        )


class Caso3Regresion(CasoRegresion):
    def obtener_datos(self):
        return (
            [163, 765, 141, 166, 137, 355, 136, 1206, 433, 1130],
            [186, 699, 132, 272, 291, 331, 199, 1890, 788, 1601],
            386,
        )


class Caso4Regresion(CasoRegresion):
    def obtener_datos(self):
        return (
            [163, 765, 141, 166, 137, 355, 136, 1206, 433, 1130],
            [15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2],
            386,
        )


class VentanaBaseRegresion(QMainWindow):
    def __init__(self, archivo_ui):
        super().__init__()
        self.modelo = None
        self._cargar_interfaz(archivo_ui)
        self._conectar_eventos_base()

    def _cargar_interfaz(self, archivo_ui):
        ruta_ui = Path(__file__).resolve().parent.parent / "gui" / archivo_ui
        uic.loadUi(str(ruta_ui), self)

    def _conectar_eventos_base(self):
        self.btn_calcular.clicked.connect(self.calcular)

    def limpiar_tabla(self):
        self.tabla_datos.clearContents()

    def cargar_datos(self, x, y):
        total_filas = max(len(x), len(y))
        if self.tabla_datos.rowCount() < total_filas:
            self.tabla_datos.setRowCount(total_filas)

        self.limpiar_tabla()
        for i, (valor_x, valor_y) in enumerate(zip(x, y)):
            self.tabla_datos.setItem(i, 0, QTableWidgetItem(str(valor_x)))
            self.tabla_datos.setItem(i, 1, QTableWidgetItem(str(valor_y)))

    def leer_tabla(self):
        x = []
        y = []

        for fila in range(self.tabla_datos.rowCount()):
            item_x = self.tabla_datos.item(fila, 0)
            item_y = self.tabla_datos.item(fila, 1)

            if item_x and item_y:
                try:
                    x.append(float(item_x.text()))
                    y.append(float(item_y.text()))
                except ValueError:
                    pass

        return x, y

    def leer_xk(self):
        if hasattr(self.input_xk, "text"):
            texto_xk = self.input_xk.text()
        else:
            texto_xk = self.input_xk.toPlainText()

        if texto_xk.strip() == "":
            raise ValueError("Ingresa un valor para XK")

        return float(texto_xk)

    def cargar_xk(self, xk):
        if hasattr(self.input_xk, "setText"):
            self.input_xk.setText(str(xk))
        else:
            self.input_xk.setPlainText(str(xk))

    def mostrar_resultados(self, b1, b0, r, r2, yk):
        self.lbl_b1.setText(f"{b1:.4f}")
        self.lbl_b0.setText(f"{b0:.4f}")
        self.lbl_r.setText(f"{r:.4f}")
        self.lbl_r2.setText(f"{r2:.4f}")
        self.lbl_yk.setText(f"{yk:.4f}")

    def mostrar_error(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)

    def calcular(self):
        raise NotImplementedError("La subclase debe implementar el cálculo.")


class VentanaRegresion(VentanaBaseRegresion):
    def __init__(self):
        super().__init__("ventana_regresion.ui")
        self.casos = {
            self.btn_caso1: Caso1Regresion(),
            self.btn_caso2: Caso2Regresion(),
            self.btn_caso3: Caso3Regresion(),
            self.btn_caso4: Caso4Regresion(),
        }
        self._conectar_casos()

    def _conectar_casos(self):
        for boton, caso in self.casos.items():
            boton.clicked.connect(lambda _, caso_actual=caso: caso_actual.cargar_en_tabla(self))

    def cargar_caso(self, caso):
        caso.cargar_en_tabla(self)

    def caso1(self):
        self.cargar_caso(Caso1Regresion())

    def caso2(self):
        self.cargar_caso(Caso2Regresion())

    def caso3(self):
        self.cargar_caso(Caso3Regresion())

    def caso4(self):
        self.cargar_caso(Caso4Regresion())

    def crear_modelo(self, x, y):
        return RegresionLineal(x, y)

    def calcular(self):
        try:
            x, y = self.leer_tabla()

            if len(x) < 2:
                raise ValueError("Se necesitan al menos dos pares de datos.")

            self.modelo = self.crear_modelo(x, y)

            b1 = self.modelo.calcular_b1()
            b0 = self.modelo.calcular_b0()
            r = self.modelo.calcular_r()
            r2 = self.modelo.calcular_r2()
            xk = self.leer_xk()
            yk = self.modelo.predecir(xk)

            self.mostrar_resultados(b1, b0, r, r2, yk)

        except Exception as error:
            self.mostrar_error(str(error))


class LanzadorVentanaBase:
    def __init__(self, ventana_cls):
        self.ventana_cls = ventana_cls

    def crear_ventana(self):
        return self.ventana_cls()

    def ejecutar(self):
        app = QApplication(sys.argv)
        ventana = self.crear_ventana()
        ventana.show()
        return app.exec_()


class LanzadorVentanaRegresion(LanzadorVentanaBase):
    def __init__(self):
        super().__init__(VentanaRegresion)


if __name__ == "__main__":
    sys.exit(LanzadorVentanaRegresion().ejecutar())
