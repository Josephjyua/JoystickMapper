import json
import os


class Config:

    def __init__(self, path=None):
        if path is None:
            path = self.obtener_ruta_config()

        self.path = path
        self.profile_path = None

        self.data = self.cargar_archivo(
            self.path
        )

    def obtener_ruta_base(self):
        return os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

    def obtener_ruta_config(self):
        return os.path.join(
            self.obtener_ruta_base(),
            "config.json"
        )

    def obtener_ruta_perfiles(self):
        return os.path.join(
            self.obtener_ruta_base(),
            "profiles"
        )

    def cargar_archivo(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"No existe configuración: {path}"
            )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as archivo:
            return json.load(
                archivo
            )

    def cargar(self):
        ruta = (
            self.profile_path
            if self.profile_path
            else self.path
        )

        return self.cargar_archivo(
            ruta
        )

    def usar_perfil(self, nombre):
        ruta = os.path.join(
            self.obtener_ruta_perfiles(),
            f"{nombre}.json"
        )

        if not os.path.exists(ruta):
            raise FileNotFoundError(
                f"No existe el perfil: {nombre}"
            )

        self.profile_path = ruta

        self.data = self.cargar_archivo(
            ruta
        )

    def usar_config_global(self):
        self.profile_path = None

        self.data = self.cargar_archivo(
            self.path
        )

    def guardar(self):
        ruta = (
            self.profile_path
            if self.profile_path
            else self.path
        )

        with open(
            ruta,
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                self.data,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    def reload(self):
        self.data = self.cargar()

    def obtener_ultimo_perfil(self):
        config_global = self.cargar_archivo(
            self.path
        )

        return config_global.get(
            "ultimo_perfil"
        )

    def guardar_ultimo_perfil(self, nombre):
        config_global = self.cargar_archivo(
            self.path
        )

        config_global[
            "ultimo_perfil"
        ] = nombre

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                config_global,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    def get(self, key, default=None):
        return self.data.get(
            key,
            default
        )

    def set(self, key, value):
        self.data[key] = value