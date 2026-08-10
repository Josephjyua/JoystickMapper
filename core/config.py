import json
import os


class Config:

    def __init__(self, path=None):

        if path is None:
            path = self.obtener_ruta_config()

        self.path = path
        self.data = self.cargar()


    def obtener_ruta_config(self):

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        return os.path.join(
            base_dir,
            "config.json"
        )

    def cargar(self):

        if not os.path.exists(self.path):

            raise FileNotFoundError(
                f"No existe configuración: {self.path}"
            )


        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    def guardar(self):

        with open(
            self.path,
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

    def get(self, key, default=None):

        return self.data.get(
            key,
            default
        )

    def set(self, key, value):

        self.data[key] = value