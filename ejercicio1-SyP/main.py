import os
import sys
from pathlib import Path


def asegurar_interprete_con_pyqt():
    try:
        import PyQt5  # noqa: F401
        return
    except ImportError:
        pass

    interpretes_candidatos = [
        Path("/opt/anaconda3/bin/python3"),
        Path("/opt/anaconda3/bin/python"),
    ]

    script_actual = Path(__file__).resolve()

    for interprete in interpretes_candidatos:
        if not interprete.exists():
            continue
        if Path(sys.executable).resolve() == interprete.resolve():
            continue

        os.execv(str(interprete), [str(interprete), str(script_actual), *sys.argv[1:]])

    raise SystemExit(
        "No se encontro PyQt5 en el interprete actual.\n"
        "Instala las dependencias con:\n"
        "  pip install -r requirements.txt"
    )


def configurar_qt():
    # Evita mezclar plugins heredados de otro entorno como Anaconda.
    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH", None)
    os.environ.pop("QT_PLUGIN_PATH", None)

    try:
        import PyQt5
    except ImportError:
        return

    ruta_plugins = Path(PyQt5.__file__).resolve().parent / "Qt5" / "plugins"
    ruta_platforms = ruta_plugins / "platforms"

    if ruta_platforms.exists():
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = str(ruta_platforms)

    if ruta_plugins.exists():
        os.environ["QT_PLUGIN_PATH"] = str(ruta_plugins)


asegurar_interprete_con_pyqt()
configurar_qt()

from PyQt5.QtWidgets import QApplication
from load.load_menu_principal import VentanaMenuPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaMenuPrincipal()
    ventana.show()
    sys.exit(app.exec_())
