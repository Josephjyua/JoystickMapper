import tkinter as tk
from tkinter import ttk, messagebox


class ButtonsView(ttk.Frame):

    ACCIONES = [
        "space",
        "enter",
        "esc",
        "tab",
        "shift",
        "ctrl_l",
        "alt",
        "cmd",
        "w",
        "a",
        "s",
        "d",
        "e",
        "r",
        "q",
        "f",
        "c",
        "mouse_left",
        "mouse_right"
    ]

    def __init__(self, parent, config, mapper):
        super().__init__(parent)

        self.config = config
        self.mapper = mapper
        self.joystick = mapper.joystick

        self.botones = []
        self.boton_seleccionado = None

        self.crear_interfaz()

    def crear_interfaz(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ttk.Label(
            self,
            text="Mapeo de botones",
            font=("TkDefaultFont", 14, "bold")
        ).grid(
            row=0,
            column=0,
            pady=10
        )

        frame = ttk.Frame(self)
        frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10
        )

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        for i in range(self.joystick.buttons_count()):
            accion = self.config.get(
                "mapeo_botones",
                {}
            ).get(
                str(i),
                "Sin asignar"
            )

            boton = tk.Button(
                frame,
                text=f"Botón {i}\n→ {accion}",
                width=18,
                height=3,
                command=lambda indice=i: self.seleccionar_boton(indice)
            )

            boton.grid(
                row=i // 2,
                column=i % 2,
                padx=8,
                pady=8,
                sticky="ew"
            )

            self.botones.append(boton)

        self.editor = ttk.LabelFrame(
            self,
            text="Asignación",
            padding=15
        )

        self.editor.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=10
        )

        self.editor.columnconfigure(1, weight=1)

        ttk.Label(
            self.editor,
            text="Botón:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.boton_label = ttk.Label(
            self.editor,
            text="Ninguno seleccionado"
        )

        self.boton_label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        ttk.Label(
            self.editor,
            text="Acción:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.accion = tk.StringVar()

        self.combo_accion = ttk.Combobox(
            self.editor,
            textvariable=self.accion,
            values=self.ACCIONES,
            state="readonly"
        )

        self.combo_accion.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        ttk.Button(
            self.editor,
            text="Guardar asignación",
            command=self.guardar_asignacion
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=10
        )

    def seleccionar_boton(self, indice):
        self.boton_seleccionado = indice

        mapeos = self.config.get(
            "mapeo_botones",
            {}
        )

        accion = mapeos.get(
            str(indice),
            ""
        )

        self.boton_label.config(
            text=f"Botón {indice}"
        )

        self.accion.set(accion)

        for i, boton in enumerate(self.botones):
            if i == indice:
                boton.config(
                    relief="sunken"
                )
            else:
                boton.config(
                    relief="raised"
                )

    def guardar_asignacion(self):
        if self.boton_seleccionado is None:
            messagebox.showwarning(
                "Joystick Mapper",
                "Selecciona un botón primero."
            )
            return

        accion = self.accion.get()

        if not accion:
            messagebox.showwarning(
                "Joystick Mapper",
                "Selecciona una acción."
            )
            return

        mapeos = self.config.get(
            "mapeo_botones",
            {}
        )

        mapeos[str(
            self.boton_seleccionado
        )] = accion

        self.config.set(
            "mapeo_botones",
            mapeos
        )

        self.config.guardar()
        self.mapper.reload_config()

        self.botones[
            self.boton_seleccionado
        ].config(
            text=(
                f"Botón "
                f"{self.boton_seleccionado}\n"
                f"→ {accion}"
            )
        )

        messagebox.showinfo(
            "Joystick Mapper",
            "Asignación guardada."
        )