from core.config import Config
from core.joystick import Joystick, BUTTON_DOWN, BUTTON_UP
from core.input import Input
from core.mouse import mover_mouse

import time


class Mapper:

    def __init__(self, config):

        self.config = config

        self.joystick = Joystick()

        self.input = Input()

        self.running = False

        self.reload_config()

    def procesar_ejes_teclas(self):

        for idx, regla in enumerate(self.ejes_teclas):

            eje = regla.get("eje")
            direccion = regla.get("direccion")
            accion = regla.get("accion")


            if eje >= self.joystick.axes_count():
                continue


            valor = self.joystick.get_axis(eje)

            estado_anterior = self.estado_ejes[idx]

            estado_actual = False


            if direccion == "negativo":

                estado_actual = valor < -self.deadzone


            elif direccion == "positivo":

                estado_actual = valor > self.deadzone


            elif direccion == "gatillo":

                sensibilidad_gatillo = regla.get(
                    "sensibilidad_gatillo",
                    0.2
                )

                porcentaje = (
                    valor + 1.0
                ) / 2.0

                estado_actual = (
                    porcentaje > sensibilidad_gatillo
                )


            if estado_actual != estado_anterior:

                if estado_actual:
                    self.input.press(accion)
                else:
                    self.input.release(accion)


                self.estado_ejes[idx] = estado_actual

    def procesar_mouse(self):

        rx = self.joystick.get_axis(
            self.ejes_cfg["rs_horizontal"]
        )

        ry = self.joystick.get_axis(
            self.ejes_cfg["rs_vertical"]
        )


        dx = rx if abs(rx) > self.deadzone else 0
        dy = ry if abs(ry) > self.deadzone else 0


        if dx != 0 or dy != 0:

            mover_mouse(
                dx * self.sensibilidad,
                dy * self.sensibilidad
            )

    def procesar_botones(self):

        for evento in self.joystick.events():

            if evento.type == BUTTON_DOWN:

                boton = str(evento.button)

                if boton in self.botones:

                    self.input.press(
                        self.botones[boton]
                    )


            elif evento.type == BUTTON_UP:

                boton = str(evento.button)

                if boton in self.botones:

                    self.input.release(
                        self.botones[boton]
                    )

    def liberar_estado(self):

        for idx, activo in self.estado_ejes.items():

            if activo:

                self.input.release(
                    self.ejes_teclas[idx]["accion"]
                )

    def run(self):
        print("[+] Mapper iniciado")

        self.running = True

        try:
            while self.running:
                self.joystick.update()
                self.procesar_ejes_teclas()
                self.procesar_mouse()
                self.procesar_botones()

                time.sleep(
                    self.config.get(
                        "polling_rate_ms",
                        10
                    ) / 1000
                )

        except KeyboardInterrupt:
            print("\n[+] Cerrando mapper")

        finally:
            self.running = False
            self.liberar_estado()

    def reload_config(self):

        self.config.reload()

        self.deadzone = self.config.get(
            "deadzone",
            0.15
        )

        self.sensibilidad = self.config.get(
            "sensibilidad_mouse",
            15.0
        )

        self.ejes_cfg = self.config.get(
            "ejes_config",
            {
                "rs_horizontal": 2,
                "rs_vertical": 3
            }
        )

        self.ejes_teclas = self.config.get(
            "mapeo_ejes_a_teclas",
            []
        )

        self.botones = self.config.get(
            "mapeo_botones",
            {}
        )

        self.estado_ejes = {
            i: False
            for i in range(len(self.ejes_teclas))
        }

    def stop(self):
        self.running = False