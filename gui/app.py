
import tkinter as tk
from tkinter import ttk, messagebox
import threading

from gui.joystick_view import JoystickView
from core.mapper import Mapper


class App:
    def __init__(self, config):
        self.config = config
        self.mapper = Mapper(self.config)
        self.mapper_thread = None

        self.COLORS = {
            "bg": "#121214",
            "card_bg": "#18181b",
            "card_border": "#2c2c31",
            "accent": "#8257e5",
            "accent_hover": "#996dff",
            "text": "#e1e1e6",
            "text_dim": "#7c7c8a",
            "success": "#00e676",
            "danger": "#ff5252",
            "input_bg": "#202024"
        }

        self.root = tk.Tk()
        self.root.title("Joystick Mapper - Professional Edition")
        self.root.geometry("850x600")
        self.root.minsize(700, 500)
        self.root.configure(
            bg=self.COLORS["bg"]
        )

        self.aplicar_estilos()
        self.crear_interfaz()

    def aplicar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            ".",
            background=self.COLORS["bg"],
            foreground=self.COLORS["text"],
            font=("Segoe UI", 9)
        )

        style.configure(
            "TNotebook",
            background=self.COLORS["bg"],
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background=self.COLORS["card_bg"],
            foreground=self.COLORS["text_dim"],
            padding=[12, 6],
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", self.COLORS["accent"])
            ],
            foreground=[
                ("selected", "white")
            ]
        )

        style.configure(
            "TFrame",
            background=self.COLORS["bg"]
        )

        style.configure(
            "Card.TFrame",
            background=self.COLORS["card_bg"],
            relief="flat"
        )

        style.configure(
            "TLabel",
            background=self.COLORS["card_bg"],
            foreground=self.COLORS["text"]
        )

        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 11, "bold"),
            foreground=self.COLORS["accent"]
        )

        style.configure(
            "Status.TLabel",
            font=("Segoe UI", 9, "bold")
        )

        style.configure(
            "TSeparator",
            background=self.COLORS["card_border"]
        )

    def crear_interfaz(self):
        header_frame = tk.Frame(
            self.root,
            bg=self.COLORS["card_bg"],
            height=40
        )

        header_frame.pack(
            fill="x",
            side="top"
        )

        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="JOYSTICK MAPPER",
            font=("Segoe UI", 11, "bold"),
            bg=self.COLORS["card_bg"],
            fg=self.COLORS["text"]
        )

        title_label.pack(
            side="left",
            padx=15
        )

        self.crear_barrita_estado()

        notebook = ttk.Notebook(
            self.root
        )

        notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(10, 5)
        )

        self.tab_general = ttk.Frame(
            notebook
        )

        # self.tab_mapeo = AxesView(
        #     notebook,
        #     self.config,
        #     self.mapper
        # )

        self.tab_joystick = JoystickView(
            notebook,
            self.mapper
        )

        notebook.add(
            self.tab_general,
            text=" General "
        )

        # notebook.add(
        #     self.tab_mapeo,
        #     text=" Mapeo Ejes "
        # )

        notebook.add(
            self.tab_joystick,
            text=" Joystick Visual "
        )

        self.crear_tab_general()

    def crear_tab_general(self):
        frame = self.tab_general

        card = ttk.Frame(
            frame,
            style="Card.TFrame",
            padding=15
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            card,
            text="CONFIGURACIÓN DE ENTRADA Y MOTOR",
            style="Header.TLabel"
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(0, 15)
        )

        ttk.Label(
            card,
            text="Sensibilidad Mouse:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        val_sens = self.config.get(
            "sensibilidad_mouse",
            15.0
        )

        self.sensibilidad_var = tk.DoubleVar(
            value=float(val_sens)
        )

        sens_scale = tk.Scale(
            card,
            from_=1.0,
            to=50.0,
            resolution=0.5,
            orient="horizontal",
            variable=self.sensibilidad_var,
            bg=self.COLORS["card_bg"],
            fg=self.COLORS["text"],
            highlightthickness=0,
            troughcolor=self.COLORS["input_bg"],
            activebackground=self.COLORS["accent"]
        )

        sens_scale.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=10,
            pady=5
        )

        ttk.Label(
            card,
            text="Zona Muerta (Deadzone):"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        val_dead = self.config.get(
            "deadzone",
            0.15
        )

        self.deadzone_var = tk.DoubleVar(
            value=float(val_dead)
        )

        dead_scale = tk.Scale(
            card,
            from_=0.01,
            to=0.50,
            resolution=0.01,
            orient="horizontal",
            variable=self.deadzone_var,
            bg=self.COLORS["card_bg"],
            fg=self.COLORS["text"],
            highlightthickness=0,
            troughcolor=self.COLORS["input_bg"],
            activebackground=self.COLORS["accent"]
        )

        dead_scale.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=5
        )

        ttk.Label(
            card,
            text="Polling Rate (ms):"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=5
        )

        val_poll = self.config.get(
            "polling_rate_ms",
            10
        )

        self.polling_var = tk.StringVar(
            value=str(val_poll)
        )

        polling_spin = tk.Spinbox(
            card,
            from_=1,
            to=100,
            textvariable=self.polling_var,
            bg=self.COLORS["input_bg"],
            fg=self.COLORS["text"],
            buttonbackground=self.COLORS["card_bg"],
            relief="flat",
            width=8
        )

        polling_spin.grid(
            row=3,
            column=1,
            sticky="w",
            padx=10,
            pady=5
        )

        card.columnconfigure(
            1,
            weight=1
        )

        btn_guardar = tk.Button(
            card,
            text="Guardar Cambios Generales",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLORS["accent"],
            fg="white",
            activebackground=self.COLORS["accent_hover"],
            activeforeground="white",
            bd=0,
            cursor="hand2",
            pady=6,
            command=self.guardar
        )

        btn_guardar.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(15, 0)
        )

    def crear_barrita_estado(self):
        footer = tk.Frame(
            self.root,
            bg=self.COLORS["card_bg"]
        )

        footer.pack(
            fill="x",
            side="bottom",
            ipady=4,
            ipadx=10
        )

        self.status_indicator = tk.Canvas(
            footer,
            width=12,
            height=12,
            bg=self.COLORS["card_bg"],
            highlightthickness=0
        )

        self.status_indicator.pack(
            side="left",
            padx=(10, 5)
        )

        self.dot = self.status_indicator.create_oval(
            2,
            2,
            10,
            10,
            fill=self.COLORS["danger"]
        )

        self.status_label = ttk.Label(
            footer,
            text="Motor Detenido",
            style="Status.TLabel"
        )

        self.status_label.pack(
            side="left",
            padx=5
        )

        self.btn_detener = tk.Button(
            footer,
            text="Detener Motor",
            font=("Segoe UI", 9),
            bg="#2c2c31",
            fg=self.COLORS["text"],
            activebackground=self.COLORS["card_border"],
            activeforeground="white",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.detener_mapper
        )

        self.btn_detener.pack(
            side="right",
            padx=5
        )

        self.btn_iniciar = tk.Button(
            footer,
            text="Iniciar Motor Mapper",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLORS["accent"],
            fg="white",
            activebackground=self.COLORS["accent_hover"],
            activeforeground="white",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.iniciar_mapper
        )

        self.btn_iniciar.pack(
            side="right",
            padx=5
        )

    def guardar(self):
        try:
            self.config.set(
                "sensibilidad_mouse",
                float(
                    self.sensibilidad_var.get()
                )
            )

            self.config.set(
                "deadzone",
                float(
                    self.deadzone_var.get()
                )
            )

            self.config.set(
                "polling_rate_ms",
                int(
                    self.polling_var.get()
                )
            )

            self.config.guardar()

            self.mapper.reload_config()

            messagebox.showinfo(
                "Joystick Mapper",
                "Configuración guardada correctamente."
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Valores numéricos inválidos."
            )

    def iniciar_mapper(self):
        if self.mapper.running:
            return

        self.mapper_thread = threading.Thread(
            target=self.mapper.run,
            daemon=True
        )

        self.mapper_thread.start()

        self.status_indicator.itemconfig(
            self.dot,
            fill=self.COLORS["success"]
        )

        self.status_label.config(
            text="Motor Ejecutándose",
            foreground=self.COLORS["success"]
        )

    def detener_mapper(self):
        self.mapper.stop()

        self.status_indicator.itemconfig(
            self.dot,
            fill=self.COLORS["danger"]
        )

        self.status_label.config(
            text="Motor Detenido",
            foreground=self.COLORS["text_dim"]
        )

    def run(self):
        self.root.mainloop()

