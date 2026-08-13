
import tkinter as tk
from tkinter import ttk, messagebox


class JoystickView(ttk.Frame):

    def __init__(self, parent, mapper):
        super().__init__(parent)

        self.mapper = mapper
        self.joystick = mapper.joystick
        self.config = mapper.config

        self.control_tipo = None
        self.control_seleccionado = None
        self.capturando_tecla = False

        self.elementos_canvas = {}
        self.stick_directions = {}

        self.COLORS = {
            "bg": "#121214",
            "body": "#202024",
            "body_outline": "#2c2c31",
            "btn_normal": "#29292e",
            "btn_hover": "#323238",
            "btn_active": "#00e676",
            "btn_selected": "#00b0ff",
            "text": "#e1e1e6",
            "text_dim": "#7c7c8a",
            "accent": "#8257e5"
        }

        self.crear_interfaz()
        self.actualizar()

    # ==========================================================
    # INTERFAZ
    # ==========================================================

    def crear_interfaz(self):
        self.configure(style="TFrame")

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.panel_mando = tk.Canvas(
            self,
            bg=self.COLORS["bg"],
            highlightthickness=0
        )

        self.panel_mando.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.panel_mando.bind(
            "<Configure>",
            self.dibujar_gamepad
        )

        self.crear_panel_editor()

    def crear_panel_editor(self):
        editor = tk.Frame(
            self,
            bg=self.COLORS["body"],
            bd=1,
            relief="solid"
        )

        editor.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 10),
            pady=10
        )

        tk.Label(
            editor,
            text="CONFIGURACIÓN",
            font=("Segoe UI", 12, "bold"),
            bg=self.COLORS["body"],
            fg=self.COLORS["accent"]
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        tk.Label(
            editor,
            text=self.joystick.device.get_name(),
            font=("Segoe UI", 9),
            bg=self.COLORS["body"],
            fg=self.COLORS["text_dim"],
            wraplength=220,
            justify="left"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

        card = tk.Frame(
            editor,
            bg=self.COLORS["bg"],
            padx=10,
            pady=10
        )

        card.pack(
            fill="x",
            padx=15,
            pady=5
        )

        tk.Label(
            card,
            text="Elemento seleccionado:",
            font=("Segoe UI", 8),
            bg=self.COLORS["bg"],
            fg=self.COLORS["text_dim"]
        ).pack(anchor="w")

        self.elemento_label = tk.Label(
            card,
            text="Ninguno",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLORS["bg"],
            fg=self.COLORS["text"]
        )

        self.elemento_label.pack(
            anchor="w",
            pady=(2, 8)
        )

        tk.Label(
            card,
            text="Mapeo actual:",
            font=("Segoe UI", 8),
            bg=self.COLORS["bg"],
            fg=self.COLORS["text_dim"]
        ).pack(anchor="w")

        self.accion_label = tk.Label(
            card,
            text="Sin asignar",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLORS["bg"],
            fg=self.COLORS["btn_selected"]
        )

        self.accion_label.pack(
            anchor="w",
            pady=(2, 0)
        )

        self.capturar_button = tk.Button(
            editor,
            text="Capturar Entrada",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLORS["accent"],
            fg="white",
            activebackground="#996dff",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            pady=8,
            command=self.iniciar_captura_tecla
        )

        self.capturar_button.pack(
            fill="x",
            padx=15,
            pady=(20, 5)
        )

        self.guardar_button = tk.Button(
            editor,
            text="Guardar Asignación",
            font=("Segoe UI", 9),
            bg=self.COLORS["btn_normal"],
            fg=self.COLORS["text"],
            activebackground=self.COLORS["btn_hover"],
            activeforeground="white",
            bd=0,
            cursor="hand2",
            pady=8,
            command=self.guardar_asignacion
        )

        self.guardar_button.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # ------------------------------------------------------
        # STICK DERECHO
        # ------------------------------------------------------

        tk.Label(
            editor,
            text="STICK DERECHO → MOUSE",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLORS["body"],
            fg=self.COLORS["accent"]
        ).pack(
            anchor="w",
            padx=15,
            pady=(25, 8)
        )

        tk.Label(
            editor,
            text="Horizontal → Movimiento Mouse X",
            font=("Segoe UI", 9),
            bg=self.COLORS["body"],
            fg=self.COLORS["text"]
        ).pack(
            anchor="w",
            padx=15,
            pady=2
        )

        tk.Label(
            editor,
            text="Vertical → Movimiento Mouse Y",
            font=("Segoe UI", 9),
            bg=self.COLORS["body"],
            fg=self.COLORS["text"]
        ).pack(
            anchor="w",
            padx=15,
            pady=2
        )

        
    # ==========================================================
    # DIBUJAR GAMEPAD
    # ==========================================================

    def dibujar_gamepad(self, event=None):
        canvas = self.panel_mando

        canvas.delete("all")
        self.elementos_canvas.clear()
        self.stick_directions.clear()

        w = canvas.winfo_width()
        h = canvas.winfo_height()

        if w < 100 or h < 100:
            return

        cx = w / 2
        cy = h / 2

        s = min(
            w / 520,
            h / 340
        )

        # ------------------------------------------------------
        # CHASIS
        # ------------------------------------------------------

        canvas.create_oval(
            cx - 190 * s,
            cy - 80 * s,
            cx + 190 * s,
            cy + 90 * s,
            fill=self.COLORS["body"],
            outline=self.COLORS["body_outline"],
            width=max(1, int(2 * s))
        )

        canvas.create_oval(
            cx - 170 * s,
            cy - 90 * s,
            cx - 60 * s,
            cy + 130 * s,
            fill=self.COLORS["body"],
            outline=self.COLORS["body_outline"],
            width=max(1, int(2 * s))
        )

        canvas.create_oval(
            cx + 60 * s,
            cy - 90 * s,
            cx + 170 * s,
            cy + 130 * s,
            fill=self.COLORS["body"],
            outline=self.COLORS["body_outline"],
            width=max(1, int(2 * s))
        )

        # ------------------------------------------------------
        # GATILLOS
        # ------------------------------------------------------

        lt = canvas.create_rectangle(
            cx - 150 * s,
            cy - 130* s,
            cx - 80 * s,
            cy - 110 * s,
            fill=self.COLORS["btn_normal"],
            outline=self.COLORS["body_outline"]
        )

        canvas.create_text(
            cx - 115 * s,
            cy - 120 * s,
            text="LT",
            fill=self.COLORS["text"],
            font=("Segoe UI", max(7, int(8 * s)), "bold")
        )

        self.elementos_canvas["lt"] = lt

        canvas.tag_bind(
            lt,
            "<Button-1>",
            lambda e: self.seleccionar_trigger("lt")
        )

        rt = canvas.create_rectangle(
            cx + 80 * s,
            cy - 130* s,
            cx + 150 * s,
            cy - 110 * s,
            fill=self.COLORS["btn_normal"],
            outline=self.COLORS["body_outline"]
        )

        canvas.create_text(
            cx + 115 * s,
            cy - 120 * s,
            text="RT",
            fill=self.COLORS["text"],
            font=("Segoe UI", max(7, int(8 * s)), "bold")
        )

        self.elementos_canvas["rt"] = rt

        canvas.tag_bind(
            rt,
            "<Button-1>",
            lambda e: self.seleccionar_trigger("rt")
        )

        # ------------------------------------------------------
        # STICK IZQUIERDO
        # ------------------------------------------------------

        self.stick_left_center = (
            cx - 115 * s,
            cy - 45 * s
        )

        base_left = canvas.create_oval(
            self.stick_left_center[0] - 32 * s,
            self.stick_left_center[1] - 32 * s,
            self.stick_left_center[0] + 32 * s,
            self.stick_left_center[1] + 32 * s,
            fill=self.COLORS["bg"],
            outline=self.COLORS["body_outline"]
        )

        self.elementos_canvas["stick_left"] = base_left

        canvas.tag_bind(
            base_left,
            "<Button-1>",
            lambda e: self.seleccionar_stick("left")
        )

        self.elementos_canvas["stick_left_cap"] = canvas.create_oval(
            self.stick_left_center[0] - 12 * s,
            self.stick_left_center[1] - 12 * s,
            self.stick_left_center[0] + 12 * s,
            self.stick_left_center[1] + 12 * s,
            fill="#323238",
            outline=self.COLORS["accent"],
            width=max(1, int(2 * s))
        )

        canvas.tag_bind(
            self.elementos_canvas["stick_left_cap"],
            "<Button-1>",
            lambda e: self.seleccionar_stick("left")
        )

        self.crear_controles_stick_izquierdo(
            cx,
            cy,
            s
        )

        # ------------------------------------------------------
        # STICK DERECHO
        # ------------------------------------------------------

        self.stick_right_center = (
            cx + 40 * s,
            cy + 30 * s
        )

        base_right = canvas.create_oval(
            self.stick_right_center[0] - 32 * s,
            self.stick_right_center[1] - 32 * s,
            self.stick_right_center[0] + 32 * s,
            self.stick_right_center[1] + 32 * s,
            fill=self.COLORS["bg"],
            outline=self.COLORS["body_outline"]
        )

        self.elementos_canvas["stick_right"] = base_right

        canvas.tag_bind(
            base_right,
            "<Button-1>",
            lambda e: self.seleccionar_stick("right")
        )

        self.elementos_canvas["stick_right_cap"] = canvas.create_oval(
            self.stick_right_center[0] - 12 * s,
            self.stick_right_center[1] - 12 * s,
            self.stick_right_center[0] + 12 * s,
            self.stick_right_center[1] + 12 * s,
            fill="#323238",
            outline=self.COLORS["accent"],
            width=max(1, int(2 * s))
        )

        canvas.tag_bind(
            self.elementos_canvas["stick_right_cap"],
            "<Button-1>",
            lambda e: self.seleccionar_stick("right")
        )

        # ------------------------------------------------------
        # D-PAD
        # ------------------------------------------------------

        dpad_x = cx - 120 * s
        dpad_y = cy + 55 * s

        w_dpad = 9 * s
        h_dpad = 22 * s

        pos_hats = {
            "up": (
                dpad_x - w_dpad,
                dpad_y - h_dpad,
                dpad_x + w_dpad,
                dpad_y - 5 * s
            ),
            "down": (
                dpad_x - w_dpad,
                dpad_y + 5 * s,
                dpad_x + w_dpad,
                dpad_y + h_dpad
            ),
            "left": (
                dpad_x - h_dpad,
                dpad_y - w_dpad,
                dpad_x - 5 * s,
                dpad_y + w_dpad
            ),
            "right": (
                dpad_x + 5 * s,
                dpad_y - w_dpad,
                dpad_x + h_dpad,
                dpad_y + w_dpad
            )
        }

        for direccion, coords in pos_hats.items():

            item = canvas.create_rectangle(
                *coords,
                fill=self.COLORS["btn_normal"],
                outline=self.COLORS["body_outline"]
            )

            self.elementos_canvas[
                f"hat_{direccion}"
            ] = item

            canvas.tag_bind(
                item,
                "<Button-1>",
                lambda e, d=direccion:
                self.seleccionar_hat(d)
            )

        # ------------------------------------------------------
        # BOTONES ABXY
        # ------------------------------------------------------

        btn_center_x = cx + 110 * s
        btn_center_y = cy - 20 * s

        offset = 22 * s

        layout = {
            0: (
                btn_center_x,
                btn_center_y + offset,
                "A"
            ),
            1: (
                btn_center_x + offset,
                btn_center_y,
                "B"
            ),
            2: (
                btn_center_x - offset,
                btn_center_y,
                "X"
            ),
            3: (
                btn_center_x,
                btn_center_y - offset,
                "Y"
            )
        }

        r_btn = 11 * s

        for i in range(
            self.joystick.buttons_count()
        ):

            if i in layout:
                bx, by, lbl = layout[i]
            else:
                extra_idx = i - 4

                col = extra_idx % 6
                row = extra_idx // 6

                bx = (
                    cx
                    - 75 * s
                    + col * 30 * s
                )

                by = (
                    cy
                    - 145 * s
                    - row * 24 * s
                )

                lbl = f"B{i}"

            item = canvas.create_oval(
                bx - r_btn,
                by - r_btn,
                bx + r_btn,
                by + r_btn,
                fill=self.COLORS["btn_normal"],
                outline=self.COLORS["body_outline"]
            )

            txt = canvas.create_text(
                bx,
                by,
                text=lbl,
                fill=self.COLORS["text"],
                font=(
                    "Segoe UI",
                    max(7, int(8 * s)),
                    "bold"
                )
            )

            self.elementos_canvas[
                f"btn_{i}"
            ] = item

            canvas.tag_bind(
                item,
                "<Button-1>",
                lambda e, idx=i:
                self.seleccionar_boton(idx)
            )

            canvas.tag_bind(
                txt,
                "<Button-1>",
                lambda e, idx=i:
                self.seleccionar_boton(idx)
            )

    # ==========================================================
    # CONTROLES DEL STICK IZQUIERDO
    # ==========================================================

    def crear_controles_stick_izquierdo(self, cx, cy, s):
        canvas = self.panel_mando

        center_x, center_y = self.stick_left_center

        size = 14 * s
        gap = 42 * s

        posiciones = {
            "arriba": (
                center_x,
                center_y - gap
            ),
            "abajo": (
                center_x,
                center_y + gap
            ),
            "izquierda": (
                center_x - gap,
                center_y
            ),
            "derecha": (
                center_x + gap,
                center_y
            )
        }

        simbolos = {
            "arriba": "↑",
            "abajo": "↓",
            "izquierda": "←",
            "derecha": "→"
        }

        mapeos = self.config.get(
            "mapeo_stick_izquierdo",
            {
                "arriba": "w",
                "abajo": "s",
                "izquierda": "a",
                "derecha": "d"
            }
        )

        for direccion, (x, y) in posiciones.items():

            item = canvas.create_rectangle(
                x - size,
                y - size,
                x + size,
                y + size,
                fill=self.COLORS["btn_normal"],
                outline=self.COLORS["body_outline"],
                width=max(1, int(1 * s))
            )

            texto = mapeos.get(
                direccion,
                simbolos[direccion]
            )

            txt = canvas.create_text(
                x,
                y,
                text=texto.upper(),
                fill=self.COLORS["text"],
                font=(
                    "Segoe UI",
                    max(7, int(9 * s)),
                    "bold"
                )
            )

            self.elementos_canvas[
                f"stick_dir_{direccion}"
            ] = item

            self.stick_directions[
                direccion
            ] = txt

            canvas.tag_bind(
                item,
                "<Button-1>",
                lambda e, d=direccion:
                self.seleccionar_direccion_stick(d)
            )

            canvas.tag_bind(
                txt,
                "<Button-1>",
                lambda e, d=direccion:
                self.seleccionar_direccion_stick(d)
            )

    # ==========================================================
    # ACTUALIZACIÓN VISUAL
    # ==========================================================

    def actualizar(self):
        canvas = self.panel_mando

        w = canvas.winfo_width()
        h = canvas.winfo_height()

        if w > 100 and h > 100:

            s = min(
                w / 520,
                h / 340
            )

            num_ejes = self.joystick.axes_count()

            # --------------------------------------------------
            # STICK IZQUIERDO
            # --------------------------------------------------

            if num_ejes >= 2:

                lx = self.joystick.get_axis(0)
                ly = self.joystick.get_axis(1)

                if "stick_left_cap" in self.elementos_canvas:

                    px = (
                        self.stick_left_center[0]
                        + lx * 15 * s
                    )

                    py = (
                        self.stick_left_center[1]
                        + ly * 15 * s
                    )

                    canvas.coords(
                        self.elementos_canvas[
                            "stick_left_cap"
                        ],
                        px - 12 * s,
                        py - 12 * s,
                        px + 12 * s,
                        py + 12 * s
                    )

            # --------------------------------------------------
            # STICK DERECHO
            # --------------------------------------------------

            if num_ejes >= 4:

                rx = self.joystick.get_axis(2)
                ry = self.joystick.get_axis(3)

                if "stick_right_cap" in self.elementos_canvas:

                    px = (
                        self.stick_right_center[0]
                        + rx * 15 * s
                    )

                    py = (
                        self.stick_right_center[1]
                        + ry * 15 * s
                    )

                    canvas.coords(
                        self.elementos_canvas[
                            "stick_right_cap"
                        ],
                        px - 12 * s,
                        py - 12 * s,
                        px + 12 * s,
                        py + 12 * s
                    )

            # --------------------------------------------------
            # LT / RT
            # --------------------------------------------------

            lt_presionado = False
            rt_presionado = False

            if num_ejes >= 5:

                valor_lt = self.joystick.get_axis(4)

                porcentaje_lt = (
                    valor_lt + 1.0
                ) / 2.0

                lt_presionado = (
                    porcentaje_lt >= 0.2
                )

            if num_ejes >= 6:

                valor_rt = self.joystick.get_axis(5)

                porcentaje_rt = (
                    valor_rt + 1.0
                ) / 2.0

                rt_presionado = (
                    porcentaje_rt >= 0.2
                )

            self.actualizar_color_control(
                "lt",
                lt_presionado
            )

            self.actualizar_color_control(
                "rt",
                rt_presionado
            )

            # --------------------------------------------------
            # BOTONES
            # --------------------------------------------------

            for i in range(
                self.joystick.buttons_count()
            ):

                tag = self.elementos_canvas.get(
                    f"btn_{i}"
                )

                if not tag:
                    continue

                activo = self.joystick.get_button(i)

                if activo:

                    canvas.itemconfig(
                        tag,
                        fill=self.COLORS["btn_active"]
                    )

                elif (
                    self.control_tipo == "boton"
                    and str(i)
                    == self.control_seleccionado
                ):

                    canvas.itemconfig(
                        tag,
                        fill=self.COLORS["btn_selected"]
                    )

                else:

                    canvas.itemconfig(
                        tag,
                        fill=self.COLORS["btn_normal"]
                    )

            # --------------------------------------------------
            # D-PAD
            # --------------------------------------------------

            if self.joystick.hats_count() > 0:

                hx, hy = self.joystick.get_hat(0)

                estados = {
                    "up": hy > 0,
                    "down": hy < 0,
                    "left": hx < 0,
                    "right": hx > 0
                }

                for direccion, activo in estados.items():

                    tag = self.elementos_canvas.get(
                        f"hat_{direccion}"
                    )

                    if not tag:
                        continue

                    if activo:

                        canvas.itemconfig(
                            tag,
                            fill=self.COLORS["btn_active"]
                        )

                    elif (
                        self.control_tipo == "hat"
                        and direccion
                        == self.control_seleccionado
                    ):

                        canvas.itemconfig(
                            tag,
                            fill=self.COLORS["btn_selected"]
                        )

                    else:

                        canvas.itemconfig(
                            tag,
                            fill=self.COLORS["btn_normal"]
                        )

        self.after(
            30,
            self.actualizar
        )

    def actualizar_color_control(
        self,
        nombre,
        activo
    ):
        tag = self.elementos_canvas.get(nombre)

        if not tag:
            return

        if activo:

            color = self.COLORS["btn_active"]

        elif (
            self.control_tipo == "trigger"
            and self.control_seleccionado == nombre
        ):

            color = self.COLORS["btn_selected"]

        else:

            color = self.COLORS["btn_normal"]

        self.panel_mando.itemconfig(
            tag,
            fill=color
        )

    # ==========================================================
    # SELECCIÓN
    # ==========================================================

    def seleccionar_boton(self, indice):
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

        self.elemento_label.config(
            text=f"Botón {indice}"
        )

        self.accion_label.config(
            text=accion
        )

        self.actualizar_seleccion_visual()

    def seleccionar_hat(self, direccion):
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

        self.elemento_label.config(
            text=f"Cruceta {direccion.upper()}"
        )

        self.accion_label.config(
            text=accion
        )

        self.actualizar_seleccion_visual()

    def seleccionar_trigger(self, direccion):
        self.control_tipo = "trigger"
        self.control_seleccionado = direccion

        mapeos = self.config.get(
            "mapeo_gatillos",
            {}
        )

        accion = mapeos.get(
            direccion,
            "Sin asignar"
        )

        self.elemento_label.config(
            text=f"Gatillo {direccion.upper()}"
        )

        self.accion_label.config(
            text=accion
        )

        self.actualizar_seleccion_visual()

    def seleccionar_stick(self, lado):
        self.control_tipo = "stick"
        self.control_seleccionado = lado

        if lado == "left":

            self.elemento_label.config(
                text="Stick izquierdo"
            )

            self.accion_label.config(
                text="Selecciona una dirección"
            )

        else:

            self.elemento_label.config(
                text="Stick derecho"
            )

            self.accion_label.config(
                text="Mouse"
            )

        self.actualizar_seleccion_visual()

    def seleccionar_direccion_stick(self, direccion):
        self.control_tipo = "stick_direction"
        self.control_seleccionado = direccion

        mapeos = self.config.get(
            "mapeo_stick_izquierdo",
            {
                "arriba": "w",
                "abajo": "s",
                "izquierda": "a",
                "derecha": "d"
            }
        )

        accion = mapeos.get(
            direccion,
            "Sin asignar"
        )

        self.elemento_label.config(
            text=f"Stick izquierdo → {direccion.capitalize()}"
        )

        self.accion_label.config(
            text=accion
        )

        self.actualizar_seleccion_visual()

    def actualizar_seleccion_visual(self):
        for key, tag in self.elementos_canvas.items():

            if key in (
                "stick_left_cap",
                "stick_right_cap"
            ):
                continue

            self.panel_mando.itemconfig(
                tag,
                fill=self.COLORS["btn_normal"]
            )

        if self.control_tipo == "boton":

            tag = self.elementos_canvas.get(
                f"btn_{self.control_seleccionado}"
            )

            if tag:
                self.panel_mando.itemconfig(
                    tag,
                    fill=self.COLORS["btn_selected"]
                )

        elif self.control_tipo == "hat":

            tag = self.elementos_canvas.get(
                f"hat_{self.control_seleccionado}"
            )

            if tag:
                self.panel_mando.itemconfig(
                    tag,
                    fill=self.COLORS["btn_selected"]
                )

        elif self.control_tipo == "trigger":

            tag = self.elementos_canvas.get(
                self.control_seleccionado
            )

            if tag:
                self.panel_mando.itemconfig(
                    tag,
                    fill=self.COLORS["btn_selected"]
                )

        elif self.control_tipo == "stick":

            tag = self.elementos_canvas.get(
                f"stick_{self.control_seleccionado}"
            )

            if tag:
                self.panel_mando.itemconfig(
                    tag,
                    fill=self.COLORS["btn_selected"]
                )

        elif self.control_tipo == "stick_direction":

            tag = self.elementos_canvas.get(
                f"stick_dir_{self.control_seleccionado}"
            )

            if tag:
                self.panel_mando.itemconfig(
                    tag,
                    fill=self.COLORS["btn_selected"]
                )

    # ==========================================================
    # CAPTURA DE TECLADO / MOUSE
    # ==========================================================

    def iniciar_captura_tecla(self):

        if self.control_tipo is None:

            messagebox.showwarning(
                "Joystick Mapper",
                "Selecciona un control primero."
            )

            return

        if self.control_tipo == "stick":

            messagebox.showinfo(
                "Joystick Mapper",
                "Selecciona una dirección del stick izquierdo."
            )

            return

        self.accion_label.config(
            text="Presiona una tecla o botón del mouse..."
        )

        self.capturando_tecla = True

        self.root = self.winfo_toplevel()

        self.root.focus_force()

        self.root.bind(
            "<KeyPress>",
            self.capturar_tecla
        )

        self.root.bind(
            "<ButtonPress>",
            self.capturar_mouse
        )

    def capturar_tecla(self, event):

        if not self.capturando_tecla:
            return

        self.finalizar_captura()

        self.accion_label.config(
            text=event.keysym.lower()
        )

    def capturar_mouse(self, event):

        if not self.capturando_tecla:
            return

        botones = {
            1: "mouse_left",
            2: "mouse_middle",
            3: "mouse_right",
            4: "mouse_x1",
            5: "mouse_x2"
        }

        accion = botones.get(
            event.num
        )

        if not accion:
            return

        self.finalizar_captura()

        self.accion_label.config(
            text=accion
        )

    def finalizar_captura(self):

        self.capturando_tecla = False

        self.root.unbind(
            "<KeyPress>"
        )

        self.root.unbind(
            "<ButtonPress>"
        )

    # ==========================================================
    # GUARDAR ASIGNACIONES
    # ==========================================================

    def guardar_asignacion(self):

        if self.control_tipo is None:

            messagebox.showwarning(
                "Joystick Mapper",
                "Selecciona un control primero."
            )

            return

        # ------------------------------------------------------
        # STICK IZQUIERDO
        # ------------------------------------------------------

        if self.control_tipo == "stick_direction":

            accion = self.accion_label.cget(
                "text"
            )

            if accion in (
                "Sin asignar",
                "Presiona una tecla o botón del mouse...",
                "Selecciona una dirección"
            ):

                messagebox.showwarning(
                    "Joystick Mapper",
                    "Captura una tecla primero."
                )

                return

            mapeos = self.config.get(
                "mapeo_stick_izquierdo",
                {}
            )

            mapeos[
                self.control_seleccionado
            ] = accion

            self.config.set(
                "mapeo_stick_izquierdo",
                mapeos
            )

            self.config.guardar()

            self.mapper.reload_config()

            self.actualizar_texto_stick(
                self.control_seleccionado,
                accion
            )

            messagebox.showinfo(
                "Joystick Mapper",
                "Dirección del stick guardada."
            )

            return

        # ------------------------------------------------------
        # RESTO DE CONTROLES
        # ------------------------------------------------------

        if self.control_tipo == "stick":

            messagebox.showinfo(
                "Joystick Mapper",
                "Selecciona una dirección del stick izquierdo."
            )

            return

        accion = self.accion_label.cget(
            "text"
        )

        if accion in (
            "Sin asignar",
            "Presiona una tecla o botón del mouse..."
        ):

            messagebox.showwarning(
                "Joystick Mapper",
                "Captura una tecla primero."
            )

            return

        secciones = {
            "boton": "mapeo_botones",
            "hat": "mapeo_hat",
            "trigger": "mapeo_gatillos"
        }

        seccion = secciones[
            self.control_tipo
        ]

        mapeos = self.config.get(
            seccion,
            {}
        )

        mapeos[
            self.control_seleccionado
        ] = accion

        self.config.set(
            seccion,
            mapeos
        )

        self.config.guardar()

        self.mapper.reload_config()

        messagebox.showinfo(
            "Joystick Mapper",
            "Asignación guardada correctamente."
        )

    def actualizar_texto_stick(
        self,
        direccion,
        accion
    ):
        txt = self.stick_directions.get(
            direccion
        )

        if txt:

            self.panel_mando.itemconfig(
                txt,
                text=accion.upper()
            )

    # ==========================================================
    # CONFIGURACIÓN DEL MOUSE
    # ==========================================================

    def actualizar_mouse_config(self):

        ejes = self.config.get(
            "ejes_config",
            {
                "rs_horizontal": 2,
                "rs_vertical": 3
            }
        )

        ejes["mouse_enabled"] = (
            self.mouse_enabled.get()
        )

        self.config.set(
            "ejes_config",
            ejes
        )

        self.config.guardar()

        self.mapper.reload_config()

