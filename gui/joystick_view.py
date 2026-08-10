
import tkinter as tk
from tkinter import ttk


class JoystickView(ttk.Frame):

    def __init__(self, parent, mapper):
        super().__init__(parent)

        self.mapper = mapper
        self.joystick = mapper.joystick

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

        ttk.Label(
            self.contenido,
            text=self.joystick.name(),
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

        botones_frame = ttk.LabelFrame(
            self.contenido,
            text="Botones",
            padding=10
        )

        botones_frame.grid(
            row=3,
            column=0,
            padx=20,
            pady=10
        )

        for i in range(
            self.joystick.buttons_count()
        ):
            boton = tk.Label(
                botones_frame,
                text=str(i),
                width=10,
                height=2,
                relief="raised"
            )

            boton.grid(
                row=i // 4,
                column=i % 4,
                padx=5,
                pady=5
            )

            self.botones.append(boton)

        self.crear_dpad()

    def crear_dpad(self):
        if self.joystick.hats_count() == 0:
            return

        dpad_frame = ttk.LabelFrame(
            self.contenido,
            text="Cruceta",
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

        for nombre, posicion in posiciones.items():

            boton = tk.Label(
                dpad_frame,
                text=nombre.upper(),
                width=10,
                height=3,
                relief="raised"
            )

            boton.grid(
                row=posicion[0],
                column=posicion[1],
                padx=5,
                pady=5
            )

            self.hats.append(
                (nombre, boton)
            )

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
        porcentaje = (valor + 1.0) / 2.0
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

        for i, boton in enumerate(self.botones):

            presionado = self.joystick.get_button(i)

            if presionado:
                boton.config(
                    relief="sunken",
                    text=f"{i}\nPRESIONADO"
                )
            else:
                boton.config(
                    relief="raised",
                    text=str(i)
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

                if estados[nombre]:
                    boton.config(
                        relief="sunken",
                        text=f"{nombre.upper()}\nPRESIONADO"
                    )
                else:
                    boton.config(
                        relief="raised",
                        text=nombre.upper()
                    )

        self.after(
            50,
            self.actualizar
        )

