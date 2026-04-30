import sys
from pathlib import Path

from app_launcher import AplicacionPyQtBase


class AplicacionMenuPrincipal(AplicacionPyQtBase):
    def __init__(self):
        self.ruta_proyecto = Path(__file__).resolve().parent
        super().__init__(self.ruta_proyecto)

    def ruta_script(self):
        return self.ruta_proyecto / "main.py"

    def rutas_modulos(self):
        return [self.ruta_proyecto / "ejercicio1-SyP"]

    def crear_ventana(self):
        from load.load_menu_principal import VentanaMenuPrincipal

        return VentanaMenuPrincipal()


if __name__ == "__main__":
    sys.exit(AplicacionMenuPrincipal().ejecutar())
