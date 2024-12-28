import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import datetime

class SensorApp:
    def __init__(self, master):
        self.master = master
        master.title("Gestión de Sensores - Excel")

        self.df = None
        self.excel_path = None
        self.df_vigentes = None

        # Frame: Cargar y guardar
        frame_top = tk.Frame(master)
        frame_top.pack(pady=10)
        btn_cargar = tk.Button(frame_top, text="Cargar Excel", command=self.cargar_excel)
        btn_cargar.pack(side=tk.LEFT, padx=5)
        btn_guardar = tk.Button(frame_top, text="Guardar Cambios", command=self.guardar_excel)
        btn_guardar.pack(side=tk.LEFT, padx=5)

        # Campo de búsqueda
        frame_search = tk.Frame(master)
        frame_search.pack(pady=10, fill="x")
        tk.Label(frame_search, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filtrar_sensores)
        tk.Entry(frame_search, textvariable=self.search_var).pack(side=tk.LEFT, padx=5, fill="x", expand=True)

        # Treeview (listado vigentes)
        frame_tree = tk.Frame(master)
        frame_tree.pack(fill="both", expand=True)

        # INCLUIMOS SENSOR_ID en las columnas
        self.columns = (
            "SENSOR_ID",        # <-- Nueva columna
            "SERIE",
            "CAMPO",
            "GRUPO_CAMPO",
            "SENSOR",
            "SECTOR",
            "EQUIPO",
            "PROGRAMA",
            "CENTRO_COSTO",
            "PLANTACION",
            "ESPECIE",
            "VARIEDAD",
            "SUPERFICIE",
            "ESTADO",
            "CAUDAL_TEORICO",
            "CAUDAL_MAX",
            "ESTACION",
            "ESTADOSENSOR",
            "FECHA INICIO",
            "FECHA FIN",
        )
        self.tree = ttk.Treeview(frame_tree, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, stretch=True)
        self.tree.pack(fill="both", expand=True)

        vsb = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        # Cuando el usuario selecciona una fila, cargamos el detalle
        self.tree.bind("<<TreeviewSelect>>", self.cargar_detalle)

        frame_actions = tk.Frame(master)
        frame_actions.pack(pady=10)

        # Botón para mostrar vigentes
        btn_vigentes = tk.Button(frame_actions, text="Mostrar Vigentes", command=self.mostrar_vigentes)
        btn_vigentes.pack(side=tk.LEFT, padx=5)

        # Frame de edición/creación de sensor
        frame_edit = tk.LabelFrame(master, text="Editar / Crear Sensor")
        frame_edit.pack(fill="x", padx=10, pady=10)

        # Variables de edición
        # NOTA: agregamos SENSOR_ID también, si deseas dejarlo editable o no.
        self.fields_edit = {
            "SENSOR_ID":       tk.StringVar(),  # ID del sensor
            "SERIE":           tk.StringVar(),
            "CAMPO":           tk.StringVar(),
            "GRUPO_CAMPO":     tk.StringVar(),
            "SENSOR":          tk.StringVar(),
            "SECTOR":          tk.StringVar(),
            "EQUIPO":          tk.StringVar(),
            "PROGRAMA":        tk.StringVar(),
            "CENTRO_COSTO":    tk.StringVar(),
            "PLANTACION":      tk.StringVar(),
            "ESPECIE":         tk.StringVar(),
            "VARIEDAD":        tk.StringVar(),
            "SUPERFICIE":      tk.StringVar(),
            "ESTADO":          tk.StringVar(),
            "CAUDAL_TEORICO":  tk.StringVar(),
            "CAUDAL_MAX":      tk.StringVar(),
            "ESTACION":        tk.StringVar(),
            "ESTADOSENSOR":    tk.StringVar(), # 1 = vigente, 0 = no vigente
        }

        row_i = 0
        col_i = 0
        for i, (lbl, var) in enumerate(self.fields_edit.items()):
            tk.Label(frame_edit, text=lbl+":").grid(row=row_i, column=col_i*2, padx=5, pady=5, sticky='e')
            tk.Entry(frame_edit, textvariable=var).grid(row=row_i, column=col_i*2+1, padx=5, pady=5, sticky='w')
            col_i += 1
            if col_i == 4:
                col_i = 0
                row_i += 1

        # AGREGAMOS UN CAMPO EXTRA PARA ELEGIR LA FECHA FIN CON LA QUE INACTIVAREMOS EL SENSOR
        tk.Label(frame_edit, text="Fecha de inactivación (p.ej. 2024-12-31):").grid(row=row_i, column=0, padx=5, pady=5, sticky='e')
        self.fecha_inactivacion_var = tk.StringVar()
        tk.Entry(frame_edit, textvariable=self.fecha_inactivacion_var).grid(row=row_i, column=1, padx=5, pady=5, sticky='w')
        row_i += 1

        frame_buttons = tk.Frame(master)
        frame_buttons.pack(pady=10)

        btn_actualizar = tk.Button(frame_buttons, text="Actualizar Sensor", command=self.actualizar_sensor)
        btn_actualizar.pack(side=tk.LEFT, padx=5)

        btn_crear = tk.Button(frame_buttons, text="Crear Nuevo Sensor", command=self.crear_sensor)
        btn_crear.pack(side=tk.LEFT, padx=5)

    # --------------------------------------------------------------------------
    # CARGA Y GUARDA DEL EXCEL
    # --------------------------------------------------------------------------
    def cargar_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files","*.xlsx *.xls")])
        if not path:
            return
        self.excel_path = path
        print(f"Intentando cargar el archivo: {self.excel_path}")
        try:
            self.df = pd.read_excel(self.excel_path, engine="openpyxl")

            # Asegurémonos de que exista la columna SENSOR_ID
            # Si NO existe, podríamos crearla (pero idealmente ya debería existir en el Excel).
            if "SENSOR_ID" not in self.df.columns:
                self.df["SENSOR_ID"] = (
                    self.df["SERIE"].astype(str)
                    + "_"
                    + self.df["CAMPO"].astype(str)
                    + "_"
                    + self.df["GRUPO_CAMPO"].astype(str)
                    + "_"
                    + self.df["SENSOR"].astype(str)
                    + "_"
                    + self.df["CENTRO_COSTO"].astype(str)
                )

            print("Archivo cargado con éxito.")
            print("Columnas del DataFrame:", self.df.columns)
            print("Primeras 5 filas:\n", self.df.head())

            # Limpia el TreeView
            for i in self.tree.get_children():
                self.tree.delete(i)
            messagebox.showinfo("Info", "Archivo cargado con éxito.")

            # Mostramos vigentes por defecto si existen
            self.mostrar_vigentes()

        except Exception as e:
            print("Error al cargar el Excel:", e)
            messagebox.showerror("Error", f"Error al cargar el Excel: {e}")

    def guardar_excel(self):
        if self.df is None:
            messagebox.showwarning("Aviso", "No hay datos cargados.")
            return
        try:
            self.df.to_excel(self.excel_path, index=False)
            messagebox.showinfo("Info", "Cambios guardados con éxito.")
            print("Cambios guardados con éxito en", self.excel_path)
        except PermissionError:
            print("No se pudo guardar el archivo. Verificar si está abierto.")
            messagebox.showerror(
                "Error",
                "No se puede guardar el archivo. Está siendo utilizado por otro programa o no tienes permisos."
            )
        except Exception as e:
            print("Error al guardar el Excel:", e)
            messagebox.showerror("Error", f"Error al guardar el Excel: {e}")

    # --------------------------------------------------------------------------
    # MOSTRAR / FILTRAR
    # --------------------------------------------------------------------------
    def mostrar_vigentes(self):
        if self.df is None:
            print("No hay datos cargados.")
            messagebox.showwarning("Aviso", "No hay datos cargados.")
            return

        self.df.columns = self.df.columns.str.strip()

        # Chequea columnas necesarias
        columnas_necesarias = ["ESTADOSENSOR", "FECHA INICIO", "FECHA FIN"]
        for c in columnas_necesarias:
            if c not in self.df.columns:
                print(f"La columna '{c}' no está en el DataFrame.")
                messagebox.showerror("Error", f"La columna '{c}' no se encontró en el archivo.")
                return

        # Convertir FECHA FIN a datetime si no lo está
        if not pd.api.types.is_datetime64_any_dtype(self.df['FECHA FIN']):
            try:
                self.df['FECHA FIN'] = pd.to_datetime(self.df['FECHA FIN'], errors='coerce')
            except Exception as e:
                print("Error al convertir FECHA FIN:", e)
                messagebox.showerror("Error", f"Error al convertir FECHA FIN a datetime: {e}")
                return

        # Puedes filtrar por FECHA FIN == 9999-12-31 o solo ESTADOSENSOR == 1
        # EJEMPLO: filtrar solo ESTADOSENSOR=1
        self.df_vigentes = self.df[self.df['ESTADOSENSOR'] == 1].copy()

        if self.df_vigentes.empty:
            print("No se encontraron sensores vigentes.")
            messagebox.showwarning("Aviso", "No se encontraron sensores vigentes.")
        else:
            print(f"Se encontraron {len(self.df_vigentes)} registros vigentes.")

        self.actualizar_tree(self.df_vigentes)

    def actualizar_tree(self, df):
        # Limpiar tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        if df is not None and not df.empty:
            for _, row in df.iterrows():
                values = []
                for col in self.columns:
                    if col in df.columns:
                        values.append(row[col])
                    else:
                        values.append("")
                self.tree.insert("", tk.END, values=tuple(values))
        else:
            print("DataFrame vacío o nulo, no se insertan filas en el TreeView.")

    def filtrar_sensores(self, *args):
        if self.df_vigentes is None or self.df_vigentes.empty:
            print("No hay vigentes cargados para filtrar.")
            return

        filtro_text = self.search_var.get().strip().lower()
        if filtro_text == "":
            self.actualizar_tree(self.df_vigentes)
        else:
            # Puedes ajustar las columnas donde se busca
            columnas_buscar = [
                "SENSOR_ID",
                "SERIE",
                "SENSOR",
                "ESPECIE",
                "VARIEDAD",
                "EQUIPO",
                "CAMPO"
            ]
            columnas_buscar = [c for c in columnas_buscar if c in self.df_vigentes.columns]

            mask = False
            for col in columnas_buscar:
                mask = mask | self.df_vigentes[col].astype(str).str.lower().str.contains(filtro_text)

            df_filtrado = self.df_vigentes[mask]
            print(f"Filtrando con texto '{filtro_text}', encontrados {len(df_filtrado)} registros.")
            self.actualizar_tree(df_filtrado)

    # --------------------------------------------------------------------------
    # CARGAR DETALLE AL SELECCIONAR EN EL TREEVIEW
    # --------------------------------------------------------------------------
    def cargar_detalle(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])['values']
        datos = dict(zip(self.columns, item))

        for k in self.fields_edit:
            if k in datos:
                val = datos[k]
                self.fields_edit[k].set("" if pd.isna(val) else str(val))
            else:
                self.fields_edit[k].set("")

        # Deja la fecha de inactivación vacía (o con la fecha actual) por defecto
        self.fecha_inactivacion_var.set("")

    # --------------------------------------------------------------------------
    # ACTUALIZAR SENSOR (INACTIVAR Y CREAR REGISTRO NUEVO)
    # --------------------------------------------------------------------------
    def actualizar_sensor(self):
        """
        - Busca el sensor en el DataFrame por el 'SENSOR_ID'.
        - Pone la FECHA FIN deseada y ESTADOSENSOR=0 para 'inactivar' el viejo.
        - Crea uno nuevo con los datos editados y ESTADOSENSOR=1.
        - FECHA INICIO = la que desees (ej. hoy); FECHA FIN = 9999-12-31.
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Debe seleccionar un sensor vigente para actualizar.")
            return

        # Obtenemos todos los valores de la fila seleccionada en el tree
        item = self.tree.item(sel[0])['values']
        datos_originales = dict(zip(self.columns, item))

        if "SENSOR_ID" not in datos_originales:
            messagebox.showerror("Error", "No se encontró la columna 'SENSOR_ID' en el registro seleccionado.")
            return
        sensor_id_original = datos_originales["SENSOR_ID"]

        # 1) ENCONTRAR EN self.df LAS FILAS QUE TENGAN ESE SENSOR_ID Y ESTÉN VIGENTES
        #    (En la mayoría de los casos, debería haber 1 fila vigente por sensor_id).
        mask = (
            (self.df["SENSOR_ID"].astype(str) == str(sensor_id_original)) &
            (self.df["ESTADOSENSOR"] == 1)
        )
        df_vigente_idx = self.df[mask].index

        if len(df_vigente_idx) == 0:
            print("No se encontró un registro vigente con ese SENSOR_ID.")
            messagebox.showerror("Error", "No se encontró un registro vigente con ese SENSOR_ID.")
            return

        # 2) FECHA FIN PARA INACTIVAR
        #    Tomamos la fecha que el usuario ingresó (self.fecha_inactivacion_var).
        fecha_inactivacion_str = self.fecha_inactivacion_var.get().strip()
        if fecha_inactivacion_str:
            try:
                fecha_inactivacion = pd.to_datetime(fecha_inactivacion_str)
            except:
                # Si falla, usamos la fecha/hora actual
                fecha_inactivacion = datetime.datetime.now()
        else:
            # Si está vacío, inactivamos con la fecha/hora actual
            fecha_inactivacion = datetime.datetime.now()

        # 3) INACTIVAR EL ACTUAL (marcar FECHA FIN y ESTADOSENSOR=0)
        self.df.loc[df_vigente_idx, "FECHA FIN"] = fecha_inactivacion
        self.df.loc[df_vigente_idx, "ESTADOSENSOR"] = 0

        # 4) CREAR NUEVO REGISTRO (CON ESTADOSENSOR=1)
        # Tomamos los valores del formulario editado
        nuevo = {}
        # Si el usuario cambió SERIE, CAMPO, etc., se podría recalcular un NUEVO sensor_id.
        # Pero si tu lógica de negocio dice que es "el mismo sensor" con historial, 
        # convendría mantener el sensor_id original. Ajusta según tu caso.
        for c in self.df.columns:
            if c in self.fields_edit:
                valor = self.fields_edit[c].get()
                if c in ["CAUDAL_TEORICO","CAUDAL_MAX","SUPERFICIE"]:
                    try:
                        valor = float(valor)
                    except:
                        valor = pd.NA
                elif c == "ESTADOSENSOR":
                    # Forzamos a 1 en el nuevo
                    valor = 1
                elif c == "SENSOR_ID":
                    # Podemos mantener el sensor_id original si se trata del "mismo" sensor
                    valor = sensor_id_original  
                nuevo[c] = valor
            else:
                # Si esa columna no está en fields_edit, rescatamos del original
                nuevo[c] = datos_originales.get(c, None)

        # FECHA INICIO -> Podríamos usar la misma "fecha_inactivacion" + 1 día 
        # o la fecha/hora actual. Depende de tu negocio.
        fecha_hoy = datetime.datetime.now()
        nuevo["FECHA INICIO"] = fecha_hoy

        # Dejamos FECHA FIN en 9999-12-31 para indicar vigencia indefinida
        nuevo["FECHA FIN"] = datetime.datetime(9999,12,31,0,0,0)
        nuevo["ESTADOSENSOR"] = 1

        # Agregamos la nueva fila al DataFrame
        self.df = pd.concat([self.df, pd.DataFrame([nuevo])], ignore_index=True)

        print("Sensor actualizado con éxito. Se guardará el historial (old -> inactivo, new -> vigente).")
        messagebox.showinfo("Info", "Sensor actualizado con éxito.")
        self.mostrar_vigentes()

    # --------------------------------------------------------------------------
    # CREAR SENSOR (NUEVO) DESDE CERO
    # --------------------------------------------------------------------------
    def crear_sensor(self):
        """
        Crea un sensor completamente nuevo (con un nuevo ID si así se desea).
        """
        if self.df is None:
            messagebox.showwarning("Aviso", "No hay datos cargados.")
            return

        # Ejemplo: generamos un ID nuevo (uuid) o lo calculamos con la lógica actual.
        # Si preferimos un ID textual basado en SERIE + ... lo hacemos
        # Asumamos que el usuario quiere un ID textual igual a la concatenación.
        # O podrías usar un ID random con uuid.
        # new_id = str(uuid.uuid4())

        fecha_hoy = datetime.datetime.now()
        nuevo = {}
        for c in self.df.columns:
            if c in self.fields_edit:
                valor = self.fields_edit[c].get()
                if c in ["CAUDAL_TEORICO","CAUDAL_MAX","SUPERFICIE"]:
                    try:
                        valor = float(valor)
                    except:
                        valor = pd.NA
                elif c == "ESTADOSENSOR":
                    try:
                        valor = int(valor)
                    except:
                        valor = 1
                elif c == "SENSOR_ID":
                    # Si queremos recalcularlo:
                    # valor = "SERIE_CAMPO_..."  # o lo que definas
                    pass
                nuevo[c] = valor
            else:
                nuevo[c] = pd.NA

        # FECHA INICIO = hoy
        nuevo["FECHA INICIO"] = fecha_hoy
        # FECHA FIN = 9999-12-31 => vigente
        nuevo["FECHA FIN"] = datetime.datetime(9999,12,31,0,0,0)
        nuevo["ESTADOSENSOR"] = 1

        # Recalcular "SENSOR_ID" si el usuario quiere:
        if "SENSOR_ID" in nuevo:
            if not nuevo["SENSOR_ID"].strip():
                # Si viene vacío, lo calculamos
                s_serie = nuevo.get("SERIE", "X") or "X"
                s_campo = nuevo.get("CAMPO", "X") or "X"
                s_grupo = nuevo.get("GRUPO_CAMPO", "X") or "X"
                s_sensor= nuevo.get("SENSOR", "X") or "X"
                s_cc    = nuevo.get("CENTRO_COSTO", "X") or "X"
                sensor_id = f"{s_serie}_{s_campo}_{s_grupo}_{s_sensor}_{s_cc}"
                nuevo["SENSOR_ID"] = sensor_id

        self.df = pd.concat([self.df, pd.DataFrame([nuevo])], ignore_index=True)
        print("Nuevo sensor creado con éxito.")
        messagebox.showinfo("Info", "Nuevo sensor creado con éxito.")
        self.mostrar_vigentes()


if __name__ == "__main__":
    root = tk.Tk()
    app = SensorApp(root)
    root.mainloop()
