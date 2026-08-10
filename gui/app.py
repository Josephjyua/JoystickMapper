import tkinter as tk
from tkinter import ttk, messagebox
import threading

from gui.axes import AxesView
from gui.joystick_view import JoystickView
from core.mapper import Mapper
from gui.buttons import ButtonsView

class App:

    
    def __init__(self, config):
        self.config = config
        self.mapper = Mapper(self.config)
        self.mapper_thread = None

        self.root = tk.Tk()
        self.root.title("Joystick Mapper")
        self.root.geometry("800x750")
        self.root.minsize(700, 600)

        self.crear_interfaz()



    def crear_interfaz(self):
        notebook = ttk.Notebook(self.root)

        notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tab_general = ttk.Frame(notebook)

        self.tab_mapeo = AxesView(
            notebook,
            self.config,
            self.mapper
        )

        self.tab_botones = ButtonsView(
            notebook,
            self.config,
            self.mapper
        )

        self.tab_joystick = JoystickView(
            notebook,
            self.mapper
        )

        notebook.add(
            self.tab_general,
            text="General"
        )

        notebook.add(
            self.tab_mapeo,
            text="Mapeo"
        )

        notebook.add(
            self.tab_botones,
            text="Botones"
        )

        notebook.add(
            self.tab_joystick,
            text="Joystick"
        )

        self.crear_tab_general()

    def guardar(self):
        try:
            self.config.set(
                "sensibilidad_mouse",
                float(self.sensibilidad.get())
            )

            self.config.set(
                "deadzone",
                float(self.deadzone.get())
            )

            self.config.set(
                "polling_rate_ms",
                int(self.polling.get())
            )

            self.config.guardar()
            self.mapper.reload_config()

            messagebox.showinfo(
                "Joystick Mapper",
                "Configuración guardada"
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Valores inválidos"
            )

    def iniciar_mapper(self):
        if self.mapper.running:
            return

        self.mapper_thread = threading.Thread(
            target=self.mapper.run,
            daemon=True
        )

        self.mapper_thread.start()

    def detener_mapper(self):
        self.mapper.stop()

    def run(self):
        self.root.mainloop()

    def crear_tab_general(self):
        frame = self.tab_general

        frame.columnconfigure(1, weight=1)

        ttk.Label(
            frame,
            text="Sensibilidad Mouse"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        self.sensibilidad = tk.StringVar(
            value=str(
                self.config.get(
                    "sensibilidad_mouse",
                    15.0
                )
            )
        )

        ttk.Entry(
            frame,
            textvariable=self.sensibilidad
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=10,
            pady=5
        )

        ttk.Label(
            frame,
            text="Deadzone"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        self.deadzone = tk.StringVar(
            value=str(
                self.config.get(
                    "deadzone",
                    0.15
                )
            )
        )

        ttk.Entry(
            frame,
            textvariable=self.deadzone
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=10,
            pady=5
        )

        ttk.Label(
            frame,
            text="Polling (ms)"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        self.polling = tk.StringVar(
            value=str(
                self.config.get(
                    "polling_rate_ms",
                    10
                )
            )
        )

        ttk.Entry(
            frame,
            textvariable=self.polling
        ).grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=5
        )

        ttk.Separator(frame).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=15
        )

        ttk.Button(
            frame,
            text="Guardar Configuración",
            command=self.guardar
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=5
        )

        ttk.Button(
            frame,
            text="Iniciar Mapper",
            command=self.iniciar_mapper
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=5
        )

        ttk.Button(
            frame,
            text="Detener Mapper",
            command=self.detener_mapper
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=5
        )


