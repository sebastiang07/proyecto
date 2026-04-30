import sys
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
if str(RUTA_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RUTA_PROYECTO))

from app_launcher import AplicacionPyQtBase


class AplicacionEjercicio3(AplicacionPyQtBase):
    def __init__(self):
        self.ruta_ejercicio3 = Path(__file__).resolve().parent
        super().__init__(self.ruta_ejercicio3)

    def ruta_script(self):
        return self.ruta_ejercicio3 / "main.py"

    def rutas_modulos(self):
        return [self.ruta_ejercicio3]

    def crear_ventana(self):
        from load.load_ventana_integracion_inversa import VentanaIntegracionInversa

        return VentanaIntegracionInversa()


if __name__ == "__main__":
    sys.exit(AplicacionEjercicio3().ejecutar())
