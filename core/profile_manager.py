import json
import os
import re


class ProfileManager:

    PROFILE_KEYS = [
        "sensibilidad_mouse",
        "deadzone",
        "polling_rate_ms",
        "ejes_config",
        "mapeo_ejes_a_teclas",
        "mapeo_botones",
        "mapeo_hat",
        "mapeo_gatillos",
        "mapeo_stick_izquierdo",
        "sensibilidad_gatillo"
    ]

    def __init__(self, config):
        self.config = config

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.profiles_dir = os.path.join(
            base_dir,
            "profiles"
        )

        os.makedirs(
            self.profiles_dir,
            exist_ok=True
        )

        self.perfil_actual = None

    def normalizar_nombre(self, nombre):
        nombre = nombre.strip()

        nombre = re.sub(
            r'[<>:"/\\|?*]',
            "_",
            nombre
        )

        return nombre

    def ruta_perfil(self, nombre):
        nombre = self.normalizar_nombre(
            nombre
        )

        return os.path.join(
            self.profiles_dir,
            f"{nombre}.json"
        )

    def listar(self):
        perfiles = []

        for archivo in os.listdir(
            self.profiles_dir
        ):
            if not archivo.lower().endswith(
                ".json"
            ):
                continue

            perfiles.append(
                os.path.splitext(
                    archivo
                )[0]
            )

        return sorted(
            perfiles,
            key=str.lower
        )

    def existe(self, nombre):
        return os.path.isfile(
            self.ruta_perfil(nombre)
        )

    def obtener_config_actual(self):
        datos = {}

        for clave in self.PROFILE_KEYS:
            valor = self.config.get(
                clave,
                None
            )

            if valor is not None:
                datos[clave] = valor

        return datos

    def crear(self, nombre):
        nombre = self.normalizar_nombre(
            nombre
        )

        if not nombre:
            raise ValueError(
                "El nombre del perfil no puede estar vacío."
            )

        if self.existe(nombre):
            raise FileExistsError(
                "Ya existe un perfil con ese nombre."
            )

        ruta = self.ruta_perfil(
            nombre
        )

        datos = self.obtener_config_actual()

        with open(
            ruta,
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        self.config.usar_perfil(
            nombre
        )

        self.perfil_actual = nombre

        return nombre

    def cargar(self, nombre):
        nombre = self.normalizar_nombre(
            nombre
        )

        if not self.existe(nombre):
            raise FileNotFoundError(
                f"No existe el perfil: {nombre}"
            )

        self.config.usar_perfil(
            nombre
        )

        self.perfil_actual = nombre

        return self.config.data

    def guardar(self, nombre):
        nombre = self.normalizar_nombre(
            nombre
        )

        if not nombre:
            raise ValueError(
                "El nombre del perfil no puede estar vacío."
            )

        # Si estamos guardando el perfil actualmente activo,
        # Config ya sabe en qué archivo debe escribir.
        if (
            self.perfil_actual == nombre
            and self.config.profile_path is not None
        ):
            self.config.guardar()

            return nombre

        # Si se guarda con otro nombre,
        # se crea/escribe un archivo independiente.
        ruta = self.ruta_perfil(
            nombre
        )

        datos = self.obtener_config_actual()

        with open(
            ruta,
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        self.config.usar_perfil(
            nombre
        )

        self.perfil_actual = nombre

        return nombre

    def eliminar(self, nombre):
        nombre = self.normalizar_nombre(
            nombre
        )

        ruta = self.ruta_perfil(
            nombre
        )

        if not os.path.isfile(ruta):
            return False

        # Si eliminamos el perfil activo,
        # volvemos primero al config global.
        if self.perfil_actual == nombre:
            self.config.usar_config_global()
            self.perfil_actual = None

        os.remove(
            ruta
        )

        return True