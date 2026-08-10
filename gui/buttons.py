
import tkinter as tk
from tkinter import ttk, messagebox


class ButtonsView(ttk.Frame):

    def __init__(self, parent, config, mapper):
        super().__init__(parent)

        self.config = config
        self.mapper = mapper
        self.joystick = mapper.joystick

        self.botones = {}
        self.boton_anterior = {}

        self.acciones = [
            "",
            "a", "b", "c", "d", "e", "f", "g",
            "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z",
            "space",
            "shift",
            "ctrl_l",
            "alt",
            "tab",
            "enter",
            "esc",
            "mouse_left",
            "mouse_right"
        ]

        self.boton_detectado = None
        self.detectando = False

        self.crear_interfaz()
        self.actualizar()

    def crear_interfaz(self):
        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="Mapeo de botones",
            font=("TkDefaultFont", 14, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(10, 5)
        )

        ttk.Label(
            self,
            text="Presiona un botón del mando para identificarlo"
        ).grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

        self.frame_botones = ttk.Frame(self)

        self.frame_botones.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20
        )

        self.crear_botones()

        ttk.Button(
            self,
            text="Guardar mapeos",
            command=self.guardar
        ).grid(
            row=3,
            column=0,
            pady=20
        )

    def crear_botones(self):
        mapeo = self.config.get(
            "mapeo_botones",
            {}
        )

        cantidad = self.joystick.buttons_count()

        for i in range(cantidad):
            fila = i // 2
            columna = i % 2

            frame = ttk.LabelFrame(
                self.frame_botones,
                text=f"Botón {i}",
                padding=10
            )

            frame.grid(
                row=fila,
                column=columna,
                sticky="ew",
                padx=5,
                pady=5
            )

            self.frame_botones.columnconfigure(
                columna,
                weight=1
            )

            ttk.Label(
                frame,
                text="Acción:"
            ).grid(
                row=0,
                column=0,
                padx=5
            )

            variable = tk.StringVar(
                value=mapeo.get(
                    str(i),
                    ""
                )
            )

            combo = ttk.Combobox(
                frame,
                textvariable=variable,
                values=self.acciones,
                state="readonly",
                width=18
            )

            combo.grid(
                row=0,
                column=1,
                padx=5
            )

            detectar = ttk.Button(
                frame,
                text="Detectar",
                command=lambda idx=i: self.iniciar_deteccion(idx)
            )

            detectar.grid(
                row=0,
                column=2,
                padx=5
            )

            self.botones[i] = {
                "variable": variable,
                "frame": frame,
                "detectar": detectar
            }

            self.boton_anterior[i] = False

    def iniciar_deteccion(self, boton):
        if self.detectando:
            return

        self.detectando = True
        self.boton_detectado = boton

        self.botones[boton]["detectar"].config(
            text="Esperando..."
        )

        for idx, datos in self.botones.items():
            if idx != boton:
                datos["detectar"].config(
                    state="disabled"
                )

    def cancelar_deteccion(self):
        self.detectando = False
        self.boton_detectado = None

        for datos in self.botones.values():
            datos["detectar"].config(
                text="Detectar",
                state="normal"
            )

    def detectar_boton(self):
        if not self.detectando:
            return

        for boton in range(
            self.joystick.buttons_count()
        ):
            actual = self.joystick.get_button(boton)
            anterior = self.boton_anterior.get(
                boton,
                False
            )

            if actual and not anterior:
                self.botones[
                    self.boton_detectado
                ]["variable"].set(
                    str(boton)
                )

                self.cancelar_deteccion()
                return

    def actualizar_estados(self):
        for boton, datos in self.botones.items():
            presionado = self.joystick.get_button(
                boton
            )

            if presionado:
                datos["frame"].configure(
                    relief="sunken"
                )
            else:
                datos["frame"].configure(
                    relief="raised"
                )

            self.boton_anterior[boton] = presionado

    def actualizar(self):
        self.detectar_boton()
        self.actualizar_estados()

        self.after(
            50,
            self.actualizar
        )

    def guardar(self):
        mapeo = self.config.get(
            "mapeo_botones",
            {}
        ).copy()

        for boton, datos in self.botones.items():
            accion = datos["variable"].get()

            if accion:
                mapeo[str(boton)] = accion
            elif str(boton) in mapeo:
                del mapeo[str(boton)]

        self.config.set(
            "mapeo_botones",
            mapeo
        )

        self.config.guardar()
        self.mapper.reload_config()

        messagebox.showinfo(
            "Joystick Mapper",
            "Mapeos guardados"
        )

