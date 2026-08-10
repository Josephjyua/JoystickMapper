from core.joystick import Joystick
from core.joystick import BUTTON_DOWN, BUTTON_UP
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

            if eje is None or eje >= self.joystick.axes_count():
                continue

            if not accion:
                continue

            valor = self.joystick.get_axis(eje)

            estado_anterior = self.estado_ejes.get(
                idx,
                False
            )

            estado_actual = False

            if direccion == "negativo":
                estado_actual = (
                    valor < -self.deadzone
                )

            elif direccion == "positivo":
                estado_actual = (
                    valor > self.deadzone
                )

            elif direccion == "gatillo":
                sensibilidad_gatillo = regla.get(
                    "sensibilidad_gatillo",
                    self.sensibilidad_gatillo
                )

                porcentaje = (
                    valor + 1.0
                ) / 2.0

                estado_actual = (
                    porcentaje >= sensibilidad_gatillo
                )

            if estado_actual != estado_anterior:

                if estado_actual:
                    self.input.press(accion)
                else:
                    self.input.release(accion)

                self.estado_ejes[idx] = estado_actual

    def procesar_mouse(self):
        eje_x = self.ejes_cfg.get(
            "rs_horizontal"
        )

        eje_y = self.ejes_cfg.get(
            "rs_vertical"
        )

        if eje_x is None or eje_y is None:
            return

        if (
            eje_x >= self.joystick.axes_count()
            or eje_y >= self.joystick.axes_count()
        ):
            return

        rx = self.joystick.get_axis(eje_x)
        ry = self.joystick.get_axis(eje_y)

        dx = (
            rx
            if abs(rx) > self.deadzone
            else 0
        )

        dy = (
            ry
            if abs(ry) > self.deadzone
            else 0
        )

        if dx != 0 or dy != 0:
            mover_mouse(
                dx * self.sensibilidad,
                dy * self.sensibilidad
            )

    def procesar_gatillos(self):
        for nombre, eje in {
            "lt": 4,
            "rt": 5
        }.items():

            accion = self.mapeo_gatillos.get(
                nombre
            )

            if not accion:
                continue

            if eje >= self.joystick.axes_count():
                continue

            valor = self.joystick.get_axis(eje)

            porcentaje = (
                valor + 1.0
            ) / 2.0

            porcentaje = max(
                0.0,
                min(1.0, porcentaje)
            )

            presionado = (
                porcentaje >= self.sensibilidad_gatillo
            )

            estado_anterior = self.estado_gatillos.get(
                nombre,
                False
            )

            if presionado != estado_anterior:

                if presionado:
                    self.input.press(accion)
                else:
                    self.input.release(accion)

                self.estado_gatillos[nombre] = presionado

    def procesar_botones(self):
        for evento in self.joystick.events():

            if evento.type == BUTTON_DOWN:

                boton = str(
                    evento.button
                )

                accion = self.botones.get(
                    boton
                )

                if accion:
                    self.input.press(
                        accion
                    )

            elif evento.type == BUTTON_UP:

                boton = str(
                    evento.button
                )

                accion = self.botones.get(
                    boton
                )

                if accion:
                    self.input.release(
                        accion
                    )

    def procesar_hat(self):
        if self.joystick.hats_count() == 0:
            return

        x, y = self.joystick.get_hat(0)

        estados = {
            "up": y > 0,
            "down": y < 0,
            "left": x < 0,
            "right": x > 0
        }

        for direccion, activo in estados.items():

            accion = self.hats.get(
                direccion
            )

            if not accion:
                continue

            estado_anterior = self.estado_hats.get(
                direccion,
                False
            )

            if activo != estado_anterior:

                if activo:
                    self.input.press(
                        accion
                    )
                else:
                    self.input.release(
                        accion
                    )

                self.estado_hats[
                    direccion
                ] = activo

    def liberar_estado(self):

        for idx, activo in self.estado_ejes.items():

            if activo:

                accion = self.ejes_teclas[
                    idx
                ].get("accion")

                if accion:
                    self.input.release(
                        accion
                    )

        for accion in self.botones.values():

            if accion:
                self.input.release(
                    accion
                )

        for accion in self.hats.values():

            if accion:
                self.input.release(
                    accion
                )

        for nombre, activo in self.estado_gatillos.items():

            if activo:

                accion = self.mapeo_gatillos.get(
                    nombre
                )

                if accion:
                    self.input.release(
                        accion
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

                self.procesar_hat()

                self.procesar_gatillos()

                time.sleep(
                    self.config.get(
                        "polling_rate_ms",
                        10
                    ) / 1000
                )

        except KeyboardInterrupt:

            print(
                "\n[+] Cerrando mapper"
            )

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

        self.hats = self.config.get(
            "mapeo_hat",
            {}
        )

        self.mapeo_gatillos = self.config.get(
            "mapeo_gatillos",
            {}
        )

        self.sensibilidad_gatillo = self.config.get(
            "sensibilidad_gatillo",
            0.2
        )

        self.estado_ejes = {
            i: False
            for i in range(
                len(self.ejes_teclas)
            )
        }

        self.estado_hats = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }

        self.estado_gatillos = {
            "lt": False,
            "rt": False
        }

    def stop(self):
        self.running = False