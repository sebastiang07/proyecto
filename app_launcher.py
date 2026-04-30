import os
import sys
from pathlib import Path


class AplicacionPyQtBase:
    def __init__(self, ruta_base):
        self.ruta_base = Path(ruta_base).resolve()

    def asegurar_interprete_con_pyqt(self):
        try:
            import PyQt5  # noqa: F401
            return
        except ImportError:
            pass

        interpretes_candidatos = [
            Path("/opt/anaconda3/bin/python3"),
            Path("/opt/anaconda3/bin/python"),
        ]

        script_actual = self.ruta_script()

        for interprete in interpretes_candidatos:
            if not interprete.exists():
                continue
            if Path(sys.executable).resolve() == interprete.resolve():
                continue

            os.execv(str(interprete), [str(interprete), str(script_actual), *sys.argv[1:]])

        raise SystemExit(
            "No se encontro PyQt5 en el interprete actual.\n"
            "Instala las dependencias necesarias antes de ejecutar."
        )

    def configurar_qt(self):
        import PyQt5

        pyqt_dir = Path(PyQt5.__file__).resolve().parent
        plugin_path = pyqt_dir / "Qt5" / "plugins"

        if plugin_path.exists():
            os.environ.setdefault("QT_PLUGIN_PATH", str(plugin_path))
            os.environ.setdefault(
                "QT_QPA_PLATFORM_PLUGIN_PATH",
                str(plugin_path / "platforms"),
            )

    def agregar_rutas_modulos(self):
        for ruta in self.rutas_modulos():
            ruta_resuelta = str(Path(ruta).resolve())
            if ruta_resuelta not in sys.path:
                sys.path.insert(0, ruta_resuelta)

    def rutas_modulos(self):
        return []

    def ruta_script(self):
        raise NotImplementedError("La subclase debe indicar su script principal.")

    def crear_ventana(self):
        raise NotImplementedError("La subclase debe crear la ventana principal.")

    def ejecutar(self):
        self.asegurar_interprete_con_pyqt()
        self.configurar_qt()
        self.agregar_rutas_modulos()

        from PyQt5.QtWidgets import QApplication

        app = QApplication(sys.argv)
        ventana = self.crear_ventana()
        ventana.show()
        return app.exec_()
