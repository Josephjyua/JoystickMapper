import sys


if sys.platform == "win32":
    from drivers.windows import mover_mouse

elif sys.platform == "darwin":
    from drivers.macos import mover_mouse

elif sys.platform.startswith("linux"):
    from drivers.linux import mover_mouse

else:
    raise Exception(
        f"Sistema no soportado: {sys.platform}"
    )