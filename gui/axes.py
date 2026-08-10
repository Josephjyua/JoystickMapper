import tkinter as tk
from tkinter import ttk, messagebox


class AxesView(ttk.Frame):

    def __init__(self, parent, config, mapper):
        super().__init__(parent)

        self.config = config
        self.mapper = mapper

        self.crear_interfaz()
        self.cargar_datos()


    def crear_interfaz(self):

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            self,
            columns=("eje", "direccion", "accion", "sensibilidad"),
            show="headings"
        )

        self.tree.heading(
            "eje",
            text="Eje"
        )

        self.tree.heading(
            "direccion",
            text="Dirección"
        )

        self.tree.heading(
            "accion",
            text="Acción"
        )

        self.tree.heading(
            "sensibilidad",
            text="Sensibilidad"
        )

        self.tree.column(
            "eje",
            width=60,
            anchor="center"
        )

        self.tree.column(
            "direccion",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "accion",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "sensibilidad",
            width=120,
            anchor="center"
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
            pady=10
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        botones = ttk.Frame(self)

        botones.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(0, 10)
        )

        ttk.Button(
            botones,
            text="Agregar",
            command=self.agregar
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            botones,
            text="Editar",
            command=self.editar
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            botones,
            text="Eliminar",
            command=self.eliminar
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            botones,
            text="Guardar",
            command=self.guardar
        ).pack(
            side="right",
            padx=5
        )

        self.tree.bind(
            "<Double-1>",
            lambda event: self.editar()
        )


    def cargar_datos(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        reglas = self.config.get(
            "mapeo_ejes_a_teclas",
            []
        )

        for regla in reglas:

            sensibilidad = regla.get(
                "sensibilidad_gatillo",
                "-"
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    regla.get("eje", ""),
                    regla.get("direccion", ""),
                    regla.get("accion", ""),
                    sensibilidad
                )
            )


    def obtener_seleccion(self):

        seleccion = self.tree.selection()

        if not seleccion:
            messagebox.showwarning(
                "Mapeo de ejes",
                "Selecciona una regla."
            )
            return None

        return seleccion[0]


    def abrir_editor(self, valores=None):

        ventana = tk.Toplevel(self)

        ventana.title(
            "Editar eje"
            if valores
            else "Agregar eje"
        )

        ventana.geometry(
            "350x250"
        )

        ventana.transient(
            self.winfo_toplevel()
        )

        ventana.grab_set()

        ttk.Label(
            ventana,
            text="Eje"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        eje = tk.StringVar(
            value=str(valores[0])
            if valores
            else "0"
        )

        ttk.Entry(
            ventana,
            textvariable=eje
        ).pack(
            fill="x",
            padx=15
        )

        ttk.Label(
            ventana,
            text="Dirección"
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        direccion = tk.StringVar(
            value=valores[1]
            if valores
            else "negativo"
        )

        ttk.Combobox(
            ventana,
            textvariable=direccion,
            values=(
                "negativo",
                "positivo",
                "gatillo"
            ),
            state="readonly"
        ).pack(
            fill="x",
            padx=15
        )

        ttk.Label(
            ventana,
            text="Acción"
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        accion = tk.StringVar(
            value=valores[2]
            if valores
            else "a"
        )

        ttk.Entry(
            ventana,
            textvariable=accion
        ).pack(
            fill="x",
            padx=15
        )

        ttk.Label(
            ventana,
            text="Sensibilidad gatillo"
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        sensibilidad = tk.StringVar(
            value=str(valores[3])
            if valores and valores[3] != "-"
            else "0.2"
        )

        ttk.Entry(
            ventana,
            textvariable=sensibilidad
        ).pack(
            fill="x",
            padx=15
        )

        def aceptar():

            try:
                eje_num = int(eje.get())
                sens = float(sensibilidad.get())

                if eje_num < 0:
                    raise ValueError

                if not 0 <= sens <= 1:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Los valores ingresados no son válidos.",
                    parent=ventana
                )

                return

            self.tree.insert(
                "",
                "end",
                values=(
                    eje_num,
                    direccion.get(),
                    accion.get(),
                    sens
                )
            )

            ventana.destroy()

        ttk.Button(
            ventana,
            text="Aceptar",
            command=aceptar
        ).pack(
            pady=15
        )


    def agregar(self):

        self.abrir_editor()


    def editar(self):

        item = self.obtener_seleccion()

        if item is None:
            return

        valores = self.tree.item(
            item,
            "values"
        )

        ventana = tk.Toplevel(self)

        ventana.title("Editar eje")
        ventana.geometry("350x250")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        ttk.Label(
            ventana,
            text="Eje"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        eje = tk.StringVar(value=valores[0])

        ttk.Entry(
            ventana,
            textvariable=eje
        ).pack(fill="x", padx=15)

        ttk.Label(
            ventana,
            text="Dirección"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        direccion = tk.StringVar(value=valores[1])

        ttk.Combobox(
            ventana,
            textvariable=direccion,
            values=("negativo", "positivo", "gatillo"),
            state="readonly"
        ).pack(fill="x", padx=15)

        ttk.Label(
            ventana,
            text="Acción"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        accion = tk.StringVar(value=valores[2])

        ttk.Entry(
            ventana,
            textvariable=accion
        ).pack(fill="x", padx=15)

        ttk.Label(
            ventana,
            text="Sensibilidad gatillo"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        sensibilidad = tk.StringVar(
            value=valores[3] if valores[3] != "-" else "0.2"
        )

        ttk.Entry(
            ventana,
            textvariable=sensibilidad
        ).pack(fill="x", padx=15)

        def aceptar():

            try:
                eje_num = int(eje.get())
                sens = float(sensibilidad.get())

                if eje_num < 0 or not 0 <= sens <= 1:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Los valores ingresados no son válidos.",
                    parent=ventana
                )

                return

            self.tree.item(
                item,
                values=(
                    eje_num,
                    direccion.get(),
                    accion.get(),
                    sens
                )
            )

            ventana.destroy()

        ttk.Button(
            ventana,
            text="Aceptar",
            command=aceptar
        ).pack(pady=15)


    def eliminar(self):

        item = self.obtener_seleccion()

        if item is None:
            return

        confirmar = messagebox.askyesno(
            "Eliminar",
            "¿Eliminar la regla seleccionada?"
        )

        if confirmar:
            self.tree.delete(item)


    def guardar(self):

        reglas = []

        for item in self.tree.get_children():

            valores = self.tree.item(
                item,
                "values"
            )

            regla = {
                "eje": int(valores[0]),
                "direccion": valores[1],
                "accion": valores[2]
            }

            if valores[1] == "gatillo":

                regla["sensibilidad_gatillo"] = float(
                    valores[3]
                )

            reglas.append(regla)

        self.config.set(
            "mapeo_ejes_a_teclas",
            reglas
        )

        self.config.guardar()

        self.mapper.reload_config()

        messagebox.showinfo(
            "Joystick Mapper",
            "Mapeo de ejes guardado."
        )