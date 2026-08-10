import tkinter as tk
from tkinter import ttk, messagebox


class JoystickView(ttk.Frame):

    def __init__(self, parent, mapper):
        super().__init__(parent)

        self.boton_seleccionado = None
        self.control_tipo = None
        self.control_seleccionado = None
        self.capturando_tecla = False

        self.mapper = mapper
        self.joystick = mapper.joystick
        self.config = mapper.config

        self.sticks = []
        self.botones = []
        self.hats = []

        self.crear_interfaz()
        self.actualizar()

    def crear_interfaz(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.contenido = ttk.Frame(
            self.canvas,
            padding=10
        )

        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.contenido,
            anchor="nw"
        )

        self.contenido.bind(
            "<Configure>",
            self.actualizar_scroll
        )

        self.canvas.bind(
            "<Configure>",
            self.ajustar_ancho
        )

        self.crear_contenido()

    def actualizar_scroll(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def ajustar_ancho(self, event):
        self.canvas.itemconfigure(
            self.window_id,
            width=event.width
        )

    def crear_contenido(self):
        self.contenido.columnconfigure(0, weight=1)

        nombre = self.joystick.device.get_name()

        ttk.Label(
            self.contenido,
            text=nombre,
            font=("TkDefaultFont", 14, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(0, 15)
        )

        sticks_frame = ttk.Frame(
            self.contenido
        )

        sticks_frame.grid(
            row=1,
            column=0,
            pady=5
        )

        self.crear_stick(
            sticks_frame,
            "Stick Izquierdo",
            0,
            1,
            0
        )

        self.crear_stick(
            sticks_frame,
            "Stick Derecho",
            2,
            3,
            1
        )

        self.crear_triggers()

        self.crear_botones()

        self.crear_dpad()

        self.crear_editor()

    def crear_triggers(self):
        triggers_frame = ttk.LabelFrame(
            self.contenido,
            text="Gatillos",
            padding=10
        )

        triggers_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=10
        )

        self.trigger_left = ttk.Progressbar(
            triggers_frame,
            orient="horizontal",
            length=300,
            mode="determinate",
            maximum=100
        )

        self.trigger_left.grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        ttk.Label(
            triggers_frame,
            text="LT"
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        self.trigger_right = ttk.Progressbar(
            triggers_frame,
            orient="horizontal",
            length=300,
            mode="determinate",
            maximum=100
        )

        self.trigger_right.grid(
            row=1,
            column=0,
            padx=10,
            pady=5
        )

        ttk.Label(
            triggers_frame,
            text="RT"
        ).grid(
            row=1,
            column=1,
            padx=5
        )

    def crear_botones(self):
        botones_frame = ttk.LabelFrame(
            self.contenido,
            text="Botones - Haz clic para configurar",
            padding=10
        )

        botones_frame.grid(
            row=3,
            column=0,
            padx=20,
            pady=10
        )

        mapeos = self.config.get(
            "mapeo_botones",
            {}
        )

        for i in range(
            self.joystick.buttons_count()
        ):
            accion = mapeos.get(
                str(i),
                "Sin asignar"
            )

            boton = tk.Label(
                botones_frame,
                text=f"Botón {i}\n{accion}",
                width=14,
                height=3,
                relief="raised",
                borderwidth=2,
                cursor="hand2"
            )

            boton.grid(
                row=i // 4,
                column=i % 4,
                padx=5,
                pady=5
            )

            boton.bind(
                "<Button-1>",
                lambda event, indice=i:
                self.seleccionar_boton(indice)
            )

            self.botones.append(boton)

    def crear_dpad(self):
        if self.joystick.hats_count() == 0:
            return

        dpad_frame = ttk.LabelFrame(
            self.contenido,
            text="Cruceta - Haz clic para configurar",
            padding=15
        )

        dpad_frame.grid(
            row=4,
            column=0,
            pady=15
        )

        posiciones = {
            "up": (0, 1),
            "left": (1, 0),
            "right": (1, 2),
            "down": (2, 1)
        }

        mapeos = self.config.get(
            "mapeo_hat",
            {}
        )

        for nombre, posicion in posiciones.items():
            accion = mapeos.get(
                nombre,
                "Sin asignar"
            )

            boton = tk.Label(
                dpad_frame,
                text=f"{nombre.upper()}\n{accion}",
                width=12,
                height=3,
                relief="raised",
                borderwidth=2,
                cursor="hand2"
            )

            boton.grid(
                row=posicion[0],
                column=posicion[1],
                padx=5,
                pady=5
            )

            boton.bind(
                "<Button-1>",
                lambda event, direccion=nombre:
                self.seleccionar_hat(direccion)
            )

            self.hats.append(
                (nombre, boton)
            )

    def crear_editor(self):
        self.editor_frame = ttk.LabelFrame(
            self.contenido,
            text="Configuración del control",
            padding=15
        )

        self.editor_frame.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=20,
            pady=10
        )

        self.editor_frame.columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            self.editor_frame,
            text="Control seleccionado:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.boton_seleccionado_label = ttk.Label(
            self.editor_frame,
            text="Ninguno"
        )

        self.boton_seleccionado_label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        ttk.Label(
            self.editor_frame,
            text="Asignación:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.accion_label = ttk.Label(
            self.editor_frame,
            text="Sin asignar"
        )

        self.accion_label.grid(
            row=1,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        self.capturar_button = ttk.Button(
            self.editor_frame,
            text="Presionar tecla",
            command=self.iniciar_captura_tecla
        )

        self.capturar_button.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=5
        )

        self.guardar_button = ttk.Button(
            self.editor_frame,
            text="Guardar asignación",
            command=self.guardar_asignacion
        )

        self.guardar_button.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=5
        )

    def seleccionar_boton(self, indice):
        self.boton_seleccionado = indice
        self.control_tipo = "boton"
        self.control_seleccionado = str(indice)

        mapeos = self.config.get(
            "mapeo_botones",
            {}
        )

        accion = mapeos.get(
            str(indice),
            "Sin asignar"
        )

        self.boton_seleccionado_label.config(
            text=f"Botón {indice}"
        )

        self.accion_label.config(
            text=accion
        )

        self.actualizar_seleccion_visual()

    def seleccionar_hat(self, direccion):
        self.boton_seleccionado = None
        self.control_tipo = "hat"
        self.control_seleccionado = direccion

        mapeos = self.config.get(
            "mapeo_hat",
            {}
        )

        accion = mapeos.get(
            direccion,
            "Sin asignar"
        )

        self.boton_seleccionado_label.config(
            text=f"Cruceta {direccion.upper()}"
        )

        self.accion_label.config(
            text=accion
        )

        self.actualizar_seleccion_visual()

    def actualizar_seleccion_visual(self):
        for i, boton in enumerate(self.botones):
            if (
                self.control_tipo == "boton"
                and str(i) == self.control_seleccionado
            ):
                boton.config(
                    relief="sunken"
                )
            else:
                boton.config(
                    relief="raised"
                )

        for nombre, boton in self.hats:
            if (
                self.control_tipo == "hat"
                and nombre == self.control_seleccionado
            ):
                boton.config(
                    relief="sunken"
                )
            else:
                boton.config(
                    relief="raised"
                )

    def guardar_asignacion(self):
        if self.control_tipo is None:
            messagebox.showwarning(
                "Joystick Mapper",
                "Selecciona un control primero."
            )
            return

        accion = self.accion_label.cget(
            "text"
        )

        if (
            accion == "Sin asignar"
            or accion == "Presiona una tecla..."
        ):
            messagebox.showwarning(
                "Joystick Mapper",
                "Presiona una tecla primero."
            )
            return

        if self.control_tipo == "boton":
            mapeos = self.config.get(
                "mapeo_botones",
                {}
            )

            mapeos[
                self.control_seleccionado
            ] = accion

            self.config.set(
                "mapeo_botones",
                mapeos
            )

            self.config.guardar()

            self.mapper.reload_config()

            self.actualizar_texto_boton(
                int(self.control_seleccionado)
            )

        elif self.control_tipo == "hat":
            mapeos = self.config.get(
                "mapeo_hat",
                {}
            )

            mapeos[
                self.control_seleccionado
            ] = accion

            self.config.set(
                "mapeo_hat",
                mapeos
            )

            self.config.guardar()

            self.mapper.reload_config()

            self.actualizar_texto_hat(
                self.control_seleccionado
            )

        messagebox.showinfo(
            "Joystick Mapper",
            "Asignación guardada."
        )

    def actualizar_texto_boton(self, indice):
        mapeos = self.config.get(
            "mapeo_botones",
            {}
        )

        accion = mapeos.get(
            str(indice),
            "Sin asignar"
        )

        self.botones[indice].config(
            text=f"Botón {indice}\n{accion}"
        )

    def actualizar_texto_hat(self, direccion):
        mapeos = self.config.get(
            "mapeo_hat",
            {}
        )

        accion = mapeos.get(
            direccion,
            "Sin asignar"
        )

        for nombre, boton in self.hats:
            if nombre == direccion:
                boton.config(
                    text=f"{nombre.upper()}\n{accion}"
                )
                break

    def crear_stick(
        self,
        parent,
        nombre,
        eje_x,
        eje_y,
        columna
    ):
        frame = ttk.LabelFrame(
            parent,
            text=nombre,
            padding=10
        )

        frame.grid(
            row=0,
            column=columna,
            padx=15
        )

        canvas = tk.Canvas(
            frame,
            width=160,
            height=160
        )

        canvas.pack()

        canvas.create_rectangle(
            20,
            20,
            140,
            140
        )

        canvas.create_line(
            80,
            20,
            80,
            140
        )

        canvas.create_line(
            20,
            80,
            140,
            80
        )

        punto = canvas.create_oval(
            72,
            72,
            88,
            88
        )

        self.sticks.append({
            "canvas": canvas,
            "punto": punto,
            "eje_x": eje_x,
            "eje_y": eje_y
        })

    def convertir_trigger(self, valor):
        porcentaje = (
            valor + 1.0
        ) / 2.0

        porcentaje = max(
            0.0,
            min(1.0, porcentaje)
        )

        return porcentaje * 100

    def actualizar(self):
        for stick in self.sticks:
            eje_x = stick["eje_x"]
            eje_y = stick["eje_y"]

            if (
                eje_x >= self.joystick.axes_count()
                or eje_y >= self.joystick.axes_count()
            ):
                continue

            x = self.joystick.get_axis(eje_x)
            y = self.joystick.get_axis(eje_y)

            px = 80 + (x * 60)
            py = 80 + (y * 60)

            stick["canvas"].coords(
                stick["punto"],
                px - 8,
                py - 8,
                px + 8,
                py + 8
            )

        if self.joystick.axes_count() >= 6:
            lt = self.joystick.get_axis(4)
            rt = self.joystick.get_axis(5)

            self.trigger_left["value"] = (
                self.convertir_trigger(lt)
            )

            self.trigger_right["value"] = (
                self.convertir_trigger(rt)
            )

        mapeos_botones = self.config.get(
            "mapeo_botones",
            {}
        )

        for i, boton in enumerate(self.botones):
            presionado = self.joystick.get_button(i)

            if presionado:
                boton.config(
                    relief="sunken",
                    text=(
                        f"Botón {i}\n"
                        f"PRESIONADO"
                    )
                )
            else:
                accion = mapeos_botones.get(
                    str(i),
                    "Sin asignar"
                )

                boton.config(
                    relief=(
                        "sunken"
                        if (
                            self.control_tipo == "boton"
                            and str(i) == self.control_seleccionado
                        )
                        else "raised"
                    ),
                    text=(
                        f"Botón {i}\n"
                        f"{accion}"
                    )
                )

        mapeos_hat = self.config.get(
            "mapeo_hat",
            {}
        )

        if self.joystick.hats_count() > 0:
            x, y = self.joystick.get_hat(0)

            estados = {
                "up": y > 0,
                "down": y < 0,
                "left": x < 0,
                "right": x > 0
            }

            for nombre, boton in self.hats:
                accion = mapeos_hat.get(
                    nombre,
                    "Sin asignar"
                )

                if estados[nombre]:
                    boton.config(
                        relief="sunken",
                        text=(
                            f"{nombre.upper()}\n"
                            f"PRESIONADO"
                        )
                    )
                else:
                    boton.config(
                        relief=(
                            "sunken"
                            if (
                                self.control_tipo == "hat"
                                and nombre == self.control_seleccionado
                            )
                            else "raised"
                        ),
                        text=(
                            f"{nombre.upper()}\n"
                            f"{accion}"
                        )
                    )

        self.after(
            50,
            self.actualizar
        )

    def iniciar_captura_tecla(self):
        if self.control_tipo is None:
            messagebox.showwarning(
                "Joystick Mapper",
                "Selecciona un control primero."
            )
            return

        self.accion_label.config(
            text="Presiona una tecla..."
        )

        self.capturando_tecla = True

        self.root = self.winfo_toplevel()

        self.root.focus_force()

        self.root.bind(
            "<KeyPress>",
            self.capturar_tecla
        )

    def capturar_tecla(self, event):
        if not self.capturando_tecla:
            return

        self.capturando_tecla = False

        self.root.unbind(
            "<KeyPress>"
        )

        tecla = event.keysym.lower()

        self.accion_label.config(
            text=tecla
        )