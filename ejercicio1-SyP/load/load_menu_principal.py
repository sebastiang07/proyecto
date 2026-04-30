import os
import subprocess
import sys
from pathlib import Path

RUTA_EJERCICIO1 = Path(__file__).resolve().parent.parent
if str(RUTA_EJERCICIO1) not in sys.path:
    sys.path.insert(0, str(RUTA_EJERCICIO1))

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from load.load_ventana_regresion import VentanaRegresion


class VentanaMenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ventanas_hijas = []
        self._cargar_interfaz()
        self._conectar_eventos()

    def _cargar_interfaz(self):
        ruta_ui = Path(__file__).resolve().parent.parent / "gui" / "menu_principal.ui"
        uic.loadUi(str(ruta_ui), self)
        self.setWindowTitle("Menu principal")

    def _conectar_eventos(self):
        self.actionPSP_1.setMenuRole(self.actionPSP_1.NoRole)
        self.actionPSP_2.setMenuRole(self.actionPSP_2.NoRole)
        self.actionPSP_3.setMenuRole(self.actionPSP_3.NoRole)
        self.actionPSP_4.setMenuRole(self.actionPSP_4.NoRole)
        self.actionSALIR.setMenuRole(self.actionSALIR.NoRole)
        self.actionPSP_1.triggered.connect(self.abrir_ejercicio1)
        self.actionPSP_2.triggered.connect(self.abrir_ejercicio2)
        self.actionPSP_3.triggered.connect(self.abrir_ejercicio3)
        self.actionPSP_4.triggered.connect(self.abrir_ejercicio4)
        self.actionSALIR.triggered.connect(self.salir_aplicacion)

    def abrir_ejercicio1(self):
        ventana = VentanaRegresion()
        ventana.show()
        self._ventanas_hijas.append(ventana)

    def abrir_ejercicio2(self):
        self._abrir_ejercicio_externo("ejercicio2")

    def abrir_ejercicio3(self):
        self._abrir_ejercicio_externo("ejercicio3")

    def abrir_ejercicio4(self):
        self._abrir_ejercicio_externo("ejercicio4")

    def _abrir_ejercicio_externo(self, carpeta_ejercicio):
        ruta_proyecto = Path(__file__).resolve().parent.parent.parent
        ruta_ejercicio = ruta_proyecto / carpeta_ejercicio
        script_principal = ruta_ejercicio / "main.py"
        interprete_venv = ruta_ejercicio / ".venv" / "bin" / "python"

        if not script_principal.exists():
            self._mostrar_error(f"No se encontro el archivo principal de {carpeta_ejercicio}.")
            return

        interprete = interprete_venv if interprete_venv.exists() else Path(sys.executable)
        entorno = os.environ.copy()
        pythonpath_actual = entorno.get("PYTHONPATH", "")
        ruta_pythonpath = str(ruta_ejercicio)
        entorno["PYTHONPATH"] = (
            f"{ruta_pythonpath}{os.pathsep}{pythonpath_actual}"
            if pythonpath_actual
            else ruta_pythonpath
        )

        try:
            subprocess.Popen(
                [str(interprete), str(script_principal)],
                cwd=str(ruta_proyecto),
                env=entorno,
            )
        except Exception as error:
            self._mostrar_error(f"No se pudo abrir {carpeta_ejercicio}: {error}")

    def _mostrar_error(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)

    def salir_aplicacion(self):
        for ventana in self._ventanas_hijas:
            try:
                ventana.close()
            except Exception:
                pass

        QApplication.instance().quit()


class LanzadorMenuBase:
    def __init__(self, ventana_cls):
        self.ventana_cls = ventana_cls

    def crear_ventana(self):
        return self.ventana_cls()

    def ejecutar(self):
        app = QApplication(sys.argv)
        ventana = self.crear_ventana()
        ventana.show()
        return app.exec_()


class LanzadorMenuPrincipal(LanzadorMenuBase):
    def __init__(self):
        super().__init__(VentanaMenuPrincipal)


if __name__ == "__main__":
    sys.exit(LanzadorMenuPrincipal().ejecutar())
