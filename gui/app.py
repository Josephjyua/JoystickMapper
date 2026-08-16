import tkinter as tk
from tkinter import ttk, messagebox

from gui.joystick_view import JoystickView
from core.mapper import Mapper
from core.profile_manager import ProfileManager


class App:

    def __init__(self, config):
        self.config = config

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

        # IMPORTANTE EN macOS:
        # Tkinter debe iniciarse antes que pygame/SDL.
        self.root = tk.Tk()

        self.root.title(
            "Joystick Mapper - Professional Edition"
        )

        self.root.geometry(
            "850x600"
        )

        self.root.minsize(
            700,
            500
        )

        self.root.configure(
            bg=self.COLORS["bg"]
        )

        self.mapper = Mapper(
            self.config
        )

        self.profile_manager = ProfileManager(
            self.config
        )

        self.aplicar_estilos()
        self.crear_interfaz()
        self.cargar_ultimo_perfil()
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_app
        )

        self.estado_joystick_anterior = (
            self.mapper.joystick.conectado()
        )

        self.root.after(
            1000,
            self.verificar_joystick
        )

    # ==========================================================
    # JOYSTICK / RECONEXIÓN
    # ==========================================================

    def verificar_joystick(self):
        joystick = self.mapper.joystick

        conectado = (
            joystick.verificar_conexion()
        )

        if (
            conectado
            != self.estado_joystick_anterior
        ):

            if conectado:

                print(
                    f"[+] Mando conectado: "
                    f"{joystick.name()}"
                )

                self.status_indicator.itemconfig(
                    self.dot,
                    fill=self.COLORS["success"]
                )

                self.status_label.config(
                    text=(
                        f"Mando conectado: "
                        f"{joystick.name()}"
                    ),
                    foreground=self.COLORS["success"]
                )

                self.tab_joystick.actualizar_dispositivo()

            else:

                self.mapper.stop()

                self.status_indicator.itemconfig(
                    self.dot,
                    fill=self.COLORS["danger"]
                )

                self.status_label.config(
                    text="Mando desconectado",
                    foreground=self.COLORS["danger"]
                )

                self.tab_joystick.actualizar_dispositivo()

            self.estado_joystick_anterior = (
                conectado
            )

        self.root.after(
            1000,
            self.verificar_joystick
        )

    # ==========================================================
    # ESTILOS
    # ==========================================================

    def aplicar_estilos(self):
        style = ttk.Style()

        style.theme_use(
            "clam"
        )

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
                (
                    "selected",
                    self.COLORS["accent"]
                )
            ],
            foreground=[
                (
                    "selected",
                    "white"
                )
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
            background=self.COLORS["card_bg"],
            foreground=self.COLORS["accent"],
            font=("Segoe UI", 11, "bold")
        )

        style.configure(
            "Status.TLabel",
            background=self.COLORS["card_bg"],
            foreground=self.COLORS["text"],
            font=("Segoe UI", 9, "bold")
        )

        style.configure(
            "TSeparator",
            background=self.COLORS["card_border"]
        )

        # ------------------------------------------------------
        # PRIMARY BUTTON
        # ------------------------------------------------------

        style.configure(
            "Primary.TButton",
            background=self.COLORS["accent"],
            foreground="white",
            borderwidth=0,
            focusthickness=0,
            focuscolor="",
            padding=(12, 7),
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "Primary.TButton",
            background=[
                (
                    "active",
                    self.COLORS["accent_hover"]
                ),
                (
                    "pressed",
                    self.COLORS["accent_hover"]
                ),
                (
                    "disabled",
                    self.COLORS["card_border"]
                )
            ],
            foreground=[
                (
                    "active",
                    "white"
                ),
                (
                    "pressed",
                    "white"
                ),
                (
                    "disabled",
                    self.COLORS["text_dim"]
                )
            ]
        )

        # ------------------------------------------------------
        # SECONDARY BUTTON
        # ------------------------------------------------------

        style.configure(
            "Secondary.TButton",
            background=self.COLORS["card_border"],
            foreground=self.COLORS["text"],
            borderwidth=0,
            focusthickness=0,
            focuscolor="",
            padding=(12, 7),
            font=("Segoe UI", 9)
        )

        style.map(
            "Secondary.TButton",
            background=[
                (
                    "active",
                    self.COLORS["input_bg"]
                ),
                (
                    "pressed",
                    self.COLORS["input_bg"]
                )
            ],
            foreground=[
                (
                    "active",
                    "white"
                ),
                (
                    "pressed",
                    "white"
                )
            ]
        )

        # ------------------------------------------------------
        # DANGER BUTTON
        # ------------------------------------------------------

        style.configure(
            "Danger.TButton",
            background=self.COLORS["danger"],
            foreground="white",
            borderwidth=0,
            focusthickness=0,
            focuscolor="",
            padding=(12, 7),
            font=("Segoe UI", 9)
        )

        style.map(
            "Danger.TButton",
            background=[
                (
                    "active",
                    "#ff6b6b"
                ),
                (
                    "pressed",
                    "#e54848"
                )
            ],
            foreground=[
                (
                    "active",
                    "white"
                ),
                (
                    "pressed",
                    "white"
                )
            ]
        )

    # ==========================================================
    # INTERFAZ PRINCIPAL
    # ==========================================================

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

        header_frame.pack_propagate(
            False
        )

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

        # ------------------------------------------------------
        # PERFIL
        # ------------------------------------------------------

        perfil_frame = tk.Frame(
            header_frame,
            bg=self.COLORS["card_bg"]
        )

        perfil_frame.pack(
            side="right",
            padx=10
        )

        tk.Label(
            perfil_frame,
            text="Perfil:",
            bg=self.COLORS["card_bg"],
            fg=self.COLORS["text_dim"],
            font=("Segoe UI", 9)
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.perfil_var = tk.StringVar()

        self.perfil_combo = ttk.Combobox(
            perfil_frame,
            textvariable=self.perfil_var,
            state="readonly",
            width=20
        )

        self.perfil_combo.pack(
            side="left",
            padx=5
        )

        self.perfil_combo.bind(
            "<<ComboboxSelected>>",
            self.cambiar_perfil
        )

        ttk.Button(
            perfil_frame,
            text="Nuevo",
            style="Secondary.TButton",
            command=self.nuevo_perfil
        ).pack(
            side="left",
            padx=3
        )

        ttk.Button(
            perfil_frame,
            text="Guardar",
            style="Primary.TButton",
            command=self.guardar_perfil
        ).pack(
            side="left",
            padx=3
        )

        ttk.Button(
            perfil_frame,
            text="Eliminar",
            style="Danger.TButton",
            command=self.eliminar_perfil
        ).pack(
            side="left",
            padx=3
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

        self.tab_joystick = JoystickView(
            notebook,
            self.mapper
        )

        notebook.add(
            self.tab_general,
            text=" General "
        )

        notebook.add(
            self.tab_joystick,
            text=" Joystick Visual "
        )

        self.crear_tab_general()
        self.actualizar_lista_perfiles()

    # ==========================================================
    # TAB GENERAL
    # ==========================================================

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

        # ------------------------------------------------------
        # SENSIBILIDAD
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # DEADZONE
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # POLLING
        # ------------------------------------------------------

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
            5
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

        ttk.Button(
            card,
            text="Guardar Cambios Generales",
            style="Primary.TButton",
            command=self.guardar
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(15, 0)
        )

    # ==========================================================
    # FOOTER
    # ==========================================================

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

        self.btn_detener = ttk.Button(
            footer,
            text="Detener Motor",
            style="Secondary.TButton",
            command=self.detener_mapper
        )

        self.btn_detener.pack(
            side="right",
            padx=5
        )

        self.btn_iniciar = ttk.Button(
            footer,
            text="Iniciar Motor Mapper",
            style="Primary.TButton",
            command=self.iniciar_mapper
        )

        self.btn_iniciar.pack(
            side="right",
            padx=5
        )

    # ==========================================================
    # CONFIGURACIÓN GENERAL
    # ==========================================================

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

            perfil_actual = (
                self.profile_manager.perfil_actual
            )

            if perfil_actual:
                self.profile_manager.guardar(
                    perfil_actual
                )

                print(
                    f"[+] Configuración general guardada "
                    f"en perfil: {perfil_actual}"
                )

            messagebox.showinfo(
                "Joystick Mapper",
                "Configuración guardada correctamente."
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Valores numéricos inválidos."
            )

        except Exception as error:
            messagebox.showerror(
                "Joystick Mapper",
                f"No se pudo guardar la configuración:\n"
                f"{error}"
            )

    # ==========================================================
    # PERFILES
    # ==========================================================

    def actualizar_lista_perfiles(self):
        perfiles = (
            self.profile_manager.listar()
        )

        self.perfil_combo[
            "values"
        ] = perfiles

        actual = (
            self.profile_manager.perfil_actual
        )

        if actual in perfiles:
            self.perfil_var.set(
                actual
            )

    def nuevo_perfil(self):
        ventana = tk.Toplevel(
            self.root
        )

        ventana.title(
            "Nuevo perfil"
        )

        ventana.geometry(
            "320x150"
        )

        ventana.resizable(
            False,
            False
        )

        ventana.transient(
            self.root
        )

        ventana.grab_set()

        ttk.Label(
            ventana,
            text="Nombre del perfil:"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        nombre_var = tk.StringVar()

        entrada = ttk.Entry(
            ventana,
            textvariable=nombre_var
        )

        entrada.pack(
            fill="x",
            padx=15
        )

        entrada.focus_set()

        def crear():
            nombre = (
                nombre_var.get().strip()
            )

            if not nombre:
                messagebox.showwarning(
                    "Joystick Mapper",
                    "Ingresa un nombre para el perfil.",
                    parent=ventana
                )
                return

            try:
                nombre = (
                    self.profile_manager.crear(
                        nombre
                    )
                )

            except FileExistsError:
                messagebox.showwarning(
                    "Joystick Mapper",
                    "Ya existe un perfil con ese nombre.",
                    parent=ventana
                )
                return

            except ValueError as error:
                messagebox.showwarning(
                    "Joystick Mapper",
                    str(error),
                    parent=ventana
                )
                return

            self.actualizar_lista_perfiles()

            self.perfil_var.set(
                nombre
            )

            ventana.destroy()

            messagebox.showinfo(
                "Joystick Mapper",
                f"Perfil '{nombre}' creado."
            )

        ttk.Button(
            ventana,
            text="Crear perfil",
            style="Primary.TButton",
            command=crear
        ).pack(
            fill="x",
            padx=15,
            pady=15
        )

        ventana.bind(
            "<Return>",
            lambda event: crear()
        )

    def guardar_perfil(self):
        nombre = (
            self.perfil_var.get().strip()
        )

        if not nombre:
            messagebox.showwarning(
                "Joystick Mapper",
                "Selecciona o crea un perfil primero."
            )
            return

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

        except ValueError:
            messagebox.showerror(
                "Joystick Mapper",
                "Hay valores inválidos en la configuración general."
            )
            return

        self.profile_manager.guardar(
            nombre
        )

        self.mapper.reload_config()

        messagebox.showinfo(
            "Joystick Mapper",
            f"Perfil '{nombre}' guardado correctamente."
        )

    def eliminar_perfil(self):
        nombre = self.perfil_var.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Joystick Mapper",
                "Selecciona un perfil para eliminar."
            )
            return

        confirmar = messagebox.askyesno(
            "Eliminar perfil",
            f"¿Eliminar el perfil '{nombre}'?\n\n"
            "Esta acción no se puede deshacer."
        )

        if not confirmar:
            return

        eliminado = self.profile_manager.eliminar(nombre)

        if not eliminado:
            messagebox.showerror(
                "Joystick Mapper",
                "No se pudo eliminar el perfil."
            )
            return

        self.perfil_var.set("")
        self.actualizar_lista_perfiles()
        self.mapper.reload_config()

        self.sensibilidad_var.set(
            float(
                self.config.get(
                    "sensibilidad_mouse",
                    15.0
                )
            )
        )

        self.deadzone_var.set(
            float(
                self.config.get(
                    "deadzone",
                    0.15
                )
            )
        )

        self.polling_var.set(
            str(
                self.config.get(
                    "polling_rate_ms",
                    5
                )
            )
        )

        self.tab_joystick.actualizar_dispositivo()
        ultimo_perfil = (
            self.config.obtener_ultimo_perfil()
        )

        if ultimo_perfil == nombre:
            self.config.guardar_ultimo_perfil(
                None
            )

        messagebox.showinfo(
            "Joystick Mapper",
            f"Perfil '{nombre}' eliminado."
        )

    def cambiar_perfil(self, event=None):
        nuevo_perfil = self.perfil_var.get()

        if not nuevo_perfil:
            return

        perfil_actual = (
            self.profile_manager.perfil_actual
        )

        if (
            perfil_actual
            and perfil_actual != nuevo_perfil
        ):
            try:
                self.profile_manager.guardar(
                    perfil_actual
                )

                print(
                    f"[+] Perfil guardado: "
                    f"{perfil_actual}"
                )

            except Exception as error:
                messagebox.showerror(
                    "Joystick Mapper",
                    f"No se pudo guardar el perfil actual:\n"
                    f"{error}"
                )
                return

        if self.mapper.running:
            self.detener_mapper()

        try:
            self.profile_manager.cargar(nuevo_perfil)
            self.config.guardar_ultimo_perfil(nuevo_perfil)

        except FileNotFoundError:
            messagebox.showerror(
                "Joystick Mapper",
                "No se encontró el perfil seleccionado."
            )
            return

        except Exception as error:
            messagebox.showerror(
                "Joystick Mapper",
                f"No se pudo cargar el perfil:\n"
                f"{error}"
            )
            return

        self.mapper.reload_config()

        self.sensibilidad_var.set(
            float(
                self.config.get(
                    "sensibilidad_mouse",
                    15.0
                )
            )
        )

        self.deadzone_var.set(
            float(
                self.config.get(
                    "deadzone",
                    0.15
                )
            )
        )

        self.polling_var.set(
            str(
                self.config.get(
                    "polling_rate_ms",
                    5
                )
            )
        )

        # Actualizar joystick visual
        self.tab_joystick.actualizar_dispositivo()

        print(
            f"[+] Perfil cargado: "
            f"{nuevo_perfil}"
        )
    # ==========================================================
    # MOTOR
    # ==========================================================

    def iniciar_mapper(self):
        if self.mapper.running:
            return

        if not self.mapper.joystick.conectado():

            messagebox.showwarning(
                "Joystick Mapper",
                "No hay ningún mando conectado."
            )

            return

        self.mapper.iniciar()

        self.status_indicator.itemconfig(
            self.dot,
            fill=self.COLORS["success"]
        )

        self.status_label.config(
            text="Motor Ejecutándose",
            foreground=self.COLORS["success"]
        )

        self.ciclo_mapper()

    def ciclo_mapper(self):
        if not self.mapper.running:
            return

        self.mapper.procesar()

        self.root.after(
            self.config.get(
                "polling_rate_ms",
                5
            ),
            self.ciclo_mapper
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

    # ==========================================================
    # RUN
    # ==========================================================

    def run(self):
        self.root.mainloop()

    def cerrar_app(self):
        perfil_actual = (
            self.profile_manager.perfil_actual
        )

        if perfil_actual:
            try:
                self.profile_manager.guardar(
                    perfil_actual
                )

            except Exception as error:
                print(
                    f"[-] Error guardando perfil: "
                    f"{error}"
                )

        self.mapper.stop()

        self.root.destroy()

    def cargar_ultimo_perfil(self):
        ultimo_perfil = (
            self.config.obtener_ultimo_perfil()
        )

        if not ultimo_perfil:
            return

        if not self.profile_manager.existe(
            ultimo_perfil
        ):
            return

        try:
            self.profile_manager.cargar(
                ultimo_perfil
            )

            self.perfil_var.set(
                ultimo_perfil
            )

            self.mapper.reload_config()

            self.sensibilidad_var.set(
                float(
                    self.config.get(
                        "sensibilidad_mouse",
                        15.0
                    )
                )
            )

            self.deadzone_var.set(
                float(
                    self.config.get(
                        "deadzone",
                        0.15
                    )
                )
            )

            self.polling_var.set(
                str(
                    self.config.get(
                        "polling_rate_ms",
                        5
                    )
                )
            )

            self.tab_joystick.actualizar_dispositivo()

            print(
                f"[+] Perfil cargado automáticamente: "
                f"{ultimo_perfil}"
            )

        except Exception as error:
            print(
                f"[-] No se pudo cargar "
                f"el último perfil: {error}"
            )
