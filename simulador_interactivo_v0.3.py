import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import messagebox, ttk

# Constante de Coulomb exacta (N*m^2/C^2) según el modelo físico del PDF
K = 8.99e9

# --- VENTANA DE CONFIGURACIÓN SECUENCIAL COMPLETA ---
class VentanaConfiguracion:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuración del Sistema - Voltio")
        self.root.geometry("500x650")
        
        # Centrar la ventana en la pantalla del usuario
        self.root.eval('tk::PlaceWindow . center')
        
        # Variables de control de flujo
        self.cargas_configuradas = []
        self.puntos_campo_configurados = []
        self.num_cargas_objetivo = 0
        self.es_2d = True
        self.carga_actual_index = 0
        self.punto_actual_index = 0

        # Contenedor principal
        self.main_frame = ttk.Frame(root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Desplegar la fase 1 por defecto
        self.fase_dimension_y_cantidad()

    # PASO 1 y 2: Seleccionar dimensión y número de cargas
    def fase_dimension_y_cantidad(self):
        self.limpiar_pantalla_widgets()
        
        ttk.Label(self.main_frame, text="⚡ CONFIGURACIÓN INICIAL DEL SISTEMA ⚡", font=("Arial", 12, "bold")).pack(pady=15)
        
        # Selección de dimensión
        ttk.Label(self.main_frame, text="1. Seleccione la Dimensión de Trabajo:").pack(anchor=tk.W, pady=5)
        self.combo_dim = ttk.Combobox(self.main_frame, values=["1D (Sobre eje X)", "2D (Plano Cartesiano)"], state="readonly")
        self.combo_dim.pack(fill=tk.X, pady=5)
        self.combo_dim.current(1)

        # Ingreso de número de cargas
        ttk.Label(self.main_frame, text="2. Ingrese la Cantidad Total de Cargas:").pack(anchor=tk.W, pady=5)
        self.entry_num_cargas = ttk.Entry(self.main_frame)
        self.entry_num_cargas.pack(fill=tk.X, pady=5)
        self.entry_num_cargas.insert(0, "3")

        btn_siguiente = ttk.Button(self.main_frame, text="Siguiente ➔ Registrar Cargas", command=self.validar_fase_uno)
        btn_siguiente.pack(fill=tk.X, pady=30)

    def validar_fase_uno(self):
        try:
            self.num_cargas_objetivo = int(self.entry_num_cargas.get())
        except ValueError:
            messagebox.showerror("Error", "El número de cargas debe ser un entero válido.")
            return

        self.es_2d = (self.combo_dim.current() == 1)
        
        if not self.es_2d and self.num_cargas_objetivo < 2:
            messagebox.showwarning("Requisito Mínimo", "Para 1D se requieren al menos 2 cargas sobre el eje.")
            return
        elif self.es_2d and self.num_cargas_objetivo < 3:
            messagebox.showwarning("Requisito Mínimo", "Para 2D se requieren al menos 3 cargas en el plano.")
            return

        self.carga_actual_index = 0
        self.fase_captura_cargas_secuencial()

    # PASO 3: El usuario ingresa el valor y posición de cada carga
    def fase_captura_cargas_secuencial(self):
        self.limpiar_pantalla_widgets()
        
        ttk.Label(self.main_frame, text=f" REGISTRO DE CARGAS ({self.carga_actual_index + 1} de {self.num_cargas_objetivo})", font=("Arial", 11, "bold")).pack(pady=15)
        
        ttk.Label(self.main_frame, text="Valor de la Carga (µC):").pack(anchor=tk.W, pady=2)
        self.entry_q = ttk.Entry(self.main_frame)
        self.entry_q.pack(fill=tk.X, pady=5)
        self.entry_q.insert(0, "2.0" if self.carga_actual_index % 2 == 0 else "-3.0")

        ttk.Label(self.main_frame, text="Posición X (metros):").pack(anchor=tk.W, pady=2)
        self.entry_x = ttk.Entry(self.main_frame)
        self.entry_x.pack(fill=tk.X, pady=5)
        self.entry_x.insert(0, str(self.carga_actual_index * 2))

        ttk.Label(self.main_frame, text="Posición Y (metros):").pack(anchor=tk.W, pady=2)
        self.entry_y = ttk.Entry(self.main_frame)
        self.entry_y.pack(fill=tk.X, pady=5)
        if not self.es_2d:
            self.entry_y.insert(0, "0.0")
            self.entry_y.config(state="disabled")
        else:
            self.entry_y.insert(0, str((self.carga_actual_index % 2) * 2))

        btn_guardar_c = ttk.Button(self.main_frame, text="Guardar Carga ➔", command=self.guardar_carga_secuencial)
        btn_guardar_c.pack(fill=tk.X, pady=25)

    def guardar_carga_secuencial(self):
        try:
            q = float(self.entry_q.get()) * 1e-6
            x = float(self.entry_x.get())
            y = 0.0 if not self.es_2d else float(self.entry_y.get())
            nueva_pos = np.array([x, y])
            
            for i, c in enumerate(self.cargas_configuradas):
                if np.linalg.norm(c['pos'] - nueva_pos) < 0.1:
                    messagebox.showerror("Error de Posición", f"Ya existe una carga registrada en esa coordenada exacta (q{i}).")
                    return

            self.cargas_configuradas.append({'q': q, 'pos': nueva_pos})
            self.carga_actual_index += 1
            
            if self.carga_actual_index < self.num_cargas_objetivo:
                self.fase_captura_cargas_secuencial()
            else:
                self.punto_actual_index = 0
                self.fase_captura_puntos_campo_secuencial()
        except ValueError:
            messagebox.showerror("Error", "Todos los campos de posición y magnitud de carga deben ser numéricos.")

    # PASO 7: El usuario define los puntos donde desea calcular el campo eléctrico
    def fase_captura_puntos_campo_secuencial(self):
        self.limpiar_pantalla_widgets()
        
        ttk.Label(self.main_frame, text=f" PUNTOS DE CAMPO ELÉCTRICO ({self.punto_actual_index + 1} de 3)", font=("Arial", 11, "bold")).pack(pady=15)
        ttk.Label(self.main_frame, text="Establezca los puntos espaciales donde desea medir la intensidad de campo:", font=("Arial", 8, "italic"), foreground="gray").pack(pady=5)

        ttk.Label(self.main_frame, text="Coordenada X del Punto:").pack(anchor=tk.W, pady=2)
        self.entry_px = ttk.Entry(self.main_frame)
        self.entry_px.pack(fill=tk.X, pady=5)
        self.entry_px.insert(0, str(self.punto_actual_index * 2 + 1))

        ttk.Label(self.main_frame, text="Coordenada Y del Punto:").pack(anchor=tk.W, pady=2)
        self.entry_py = ttk.Entry(self.main_frame)
        self.entry_py.pack(fill=tk.X, pady=5)
        if not self.es_2d:
            self.entry_py.insert(0, "0.0")
            self.entry_py.config(state="disabled")
        else:
            self.entry_py.insert(0, "1.0" if self.punto_actual_index % 2 == 0 else "-1.0")

        btn_guardar_p = ttk.Button(self.main_frame, text="Guardar Punto de Campo ➔", command=self.guardar_punto_campo_secuencial)
        btn_guardar_p.pack(fill=tk.X, pady=25)

    def guardar_punto_campo_secuencial(self):
        try:
            px = float(self.entry_px.get())
            py = 0.0 if not self.es_2d else float(self.entry_py.get())
            nuevo_punto = [px, py]
            
            for i, carga in enumerate(self.cargas_configuradas):
                if np.linalg.norm(carga['pos'] - np.array(nuevo_punto)) < 0.1:
                    messagebox.showerror("División Entre Cero", f"No se puede medir campo eléctrico exactamente encima de la carga q{i}.")
                    return

            self.puntos_campo_configurados.append(nuevo_punto)
            self.punto_actual_index += 1
            
            if self.punto_actual_index < 3:
                self.fase_captura_puntos_campo_secuencial()
            else:
                cargas_finales = self.cargas_configuradas
                puntos_finales = self.puntos_campo_configurados
                limite = self.num_cargas_objetivo
                dim_2d = self.es_2d
                
                self.root.destroy()
                
                root_sim = tk.Tk()
                app = SimuladorGrafico(root_sim, limite, dim_2d, cargas_finales, puntos_finales)
                root_sim.mainloop()
        except ValueError:
            messagebox.showerror("Error", "Las coordenadas de los puntos de campo deben ser numéricas.")

    def limpiar_pantalla_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


# --- VENTANA PRINCIPAL DEL SIMULADOR INTERACTIVO ---
class SimuladorGrafico:
    def __init__(self, root, limite, es_2d, cargas_iniciales, puntos_iniciales):
        self.root = root
        self.root.title("Voltio - Simulador Electrostático Interactivo Pro")
        self.root.geometry("1450x780")
        
        self.es_2d = es_2d 
        self.limite_cargas = limite 
        self.cargas = cargas_iniciales  
        self.puntos_campo = puntos_iniciales  
        self.carga_seleccionada_idx = None  

        # --- PANEL IZQUIERDO: CONTROLES ---
        panel_control = ttk.LabelFrame(root, text=" Configuración del Sistema ", padding=12)
        panel_control.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)

        # INSERTAR PUNTOS DE CAMPO ELÉCTRICO DINÁMICOS
        frame_puntos = ttk.LabelFrame(panel_control, text=" Puntos de Campo Eléctrico (X) ", padding=8)
        frame_puntos.pack(fill=tk.X, pady=5)

        ttk.Label(frame_puntos, text="Punto X:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_px = ttk.Entry(frame_puntos, width=10)
        self.entry_px.grid(row=0, column=1, pady=2, padx=5)
        self.entry_px.insert(0, "2.0")

        ttk.Label(frame_puntos, text="Punto Y:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_py = ttk.Entry(frame_puntos, width=10)
        self.entry_py.grid(row=1, column=1, pady=2, padx=5)
        if not self.es_2d:
            self.entry_py.insert(0, "0.0")
            self.entry_py.config(state="disabled")
        else:
            self.entry_py.insert(0, "2.0")

        btn_agregar_p = ttk.Button(frame_puntos, text="Añadir Punto de Campo", command=self.agregar_punto_campo_gui)
        btn_agregar_p.grid(row=2, column=0, columnspan=2, sticky="ew", pady=4)
        
        btn_limpiar_p = ttk.Button(frame_puntos, text="Limpiar Puntos (X)", command=self.limpiar_puntos_campo)
        btn_limpiar_p.grid(row=3, column=0, columnspan=2, sticky="ew", pady=2)

        # EDICIÓN INDIVIDUAL
        frame_edicion = ttk.LabelFrame(panel_control, text=" Modificar Carga ", padding=8)
        frame_edicion.pack(fill=tk.X, pady=5)

        ttk.Label(frame_edicion, text="Analizar Fuerza en:").pack(anchor=tk.W, pady=2)
        self.combo_carga = ttk.Combobox(frame_edicion, state="readonly", width=12)
        self.combo_carga.pack(fill=tk.X, pady=2)
        self.combo_carga.bind("<<ComboboxSelected>>", lambda e: self.actualizar_grafica())

        ttk.Label(frame_edicion, text="Nuevo Valor (µC):").pack(anchor=tk.W, pady=2)
        self.entry_nuevo_q = ttk.Entry(frame_edicion, width=10)
        self.entry_nuevo_q.pack(fill=tk.X, pady=2)
        self.entry_nuevo_q.insert(0, "5.0")

        btn_modificar = ttk.Button(frame_edicion, text="Actualizar Valor (µC)", command=self.modificar_valor_carga)
        btn_modificar.pack(fill=tk.X, pady=4)

        btn_limpiar = ttk.Button(panel_control, text="🔄 Restablecer Arreglo Inicial", command=self.restablecer_sistema)
        btn_limpiar.pack(fill=tk.X, pady=5)

        # BOTÓN DE RETORNO AL PASO 1
        btn_volver_inicio = ttk.Button(panel_control, text="⬅ Volver a Configuración Inicial", command=self.regresar_a_config_inicial)
        btn_volver_inicio.pack(fill=tk.X, pady=10)

        # --- PANEL CENTRAL: LIENZO ---
        self.panel_grafica = ttk.Frame(root)
        self.panel_grafica.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.panel_grafica)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.panel_grafica)
        self.toolbar.update()

        self.canvas.mpl_connect("button_press_event", self.al_hacer_clic)
        self.canvas.mpl_connect("button_release_event", self.al_soltar_clic)
        self.canvas.mpl_connect("motion_notify_event", self.al_arrastrar_mouse)

        # --- PANEL DERECHO: TEXTO ---
        panel_derecho = ttk.LabelFrame(root, text=" Reporte de Resultados Matemáticos ", padding=12)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.txt_resultados = tk.Text(panel_derecho, width=45, font=("Consolas", 10))
        self.txt_resultados.pack(fill=tk.BOTH, expand=True)

        self.cargas_respaldo = [c.copy() for c in cargas_iniciales]
        self.puntos_respaldo = list(puntos_iniciales)

        self.actualizar_combo_cargas()
        if len(self.cargas) > 0: self.combo_carga.current(0)
        self.actualizar_grafica()

    def regresar_a_config_inicial(self):
        self.root.destroy() 
        root_inicio = tk.Tk()
        app = VentanaConfiguracion(root_inicio) 
        root_inicio.mainloop()

    def restablecer_sistema(self):
        self.cargas = [c.copy() for c in self.cargas_respaldo]
        self.puntos_campo = list(self.puntos_respaldo)
        self.actualizar_combo_cargas()
        self.actualizar_grafica()

    def agregar_carga_gui(self):
        if len(self.cargas) >= self.limite_cargas:
            messagebox.showwarning("Límite de Cargas", f"Has alcanzado el límite de {self.limite_cargas} cargas configuradas al inicio.")
            return
        try:
            q = float(self.entry_q.get()) * 1e-6
            x = float(self.entry_x.get())
            y = 0.0 if not self.es_2d else float(self.entry_y.get())
            nueva_pos = np.array([x, y])
            
            for i, carga in enumerate(self.cargas):
                if np.linalg.norm(carga['pos'] - nueva_pos) < 0.1:
                    messagebox.showerror("Error", f"Coincide con la posición de la carga q{i}.")
                    return

            self.cargas.append({'q': q, 'pos': nueva_pos})
            self.actualizar_combo_cargas()
            self.actualizar_grafica()
        except ValueError:
            messagebox.showerror("Error", "Coordenadas y magnitudes deben ser numéricas.")

    def modificar_valor_carga(self):
        idx = self.combo_carga.current()
        if idx == -1: return
        try:
            nuevo_q = float(self.entry_nuevo_q.get()) * 1e-6
            self.cargas[idx]['q'] = nuevo_q
            self.actualizar_grafica()
        except ValueError:
            messagebox.showerror("Error", "El valor de la carga debe ser numérico.")

    def agregar_punto_campo_gui(self):
        try:
            px = float(self.entry_px.get())
            py = 0.0 if not self.es_2d else float(self.entry_py.get())
            nuevo_punto = [px, py]
            
            for i, carga in enumerate(self.cargas):
                if np.linalg.norm(carga['pos'] - np.array(nuevo_punto)) < 0.1:
                    messagebox.showerror("Error", f"Coincide exactamente con la posición de q{i}.")
                    return
                    
            self.puntos_campo.append(nuevo_punto)
            self.actualizar_grafica()
        except ValueError:
            messagebox.showerror("Error", "Los puntos de campo deben tener coordenadas numéricas.")

    def limpiar_puntos_campo(self):
        self.puntos_campo = []
        self.actualizar_grafica()

    def actualizar_combo_cargas(self):
        valores = [f"q{i}" for i in range(len(self.cargas))]
        self.combo_carga['values'] = valores
        if valores: self.combo_carga.current(0)
        else: self.combo_carga.set('')

    def al_hacer_clic(self, event):
        if event.inaxes != self.ax or self.toolbar.mode != "": return 
        puntero = np.array([event.xdata, event.ydata])
        for i, carga in enumerate(self.cargas):
            distancia = np.linalg.norm(carga['pos'] - puntero)
            if distancia < 0.3: 
                self.carga_seleccionada_idx = i
                self.combo_carga.current(i)
                self.actualizar_grafica()
                break

    def al_arrastrar_mouse(self, event):
        if self.carga_seleccionada_idx is None or event.inaxes != self.ax: return
        nueva_pos = np.array([event.xdata, 0.0]) if not self.es_2d else np.array([event.xdata, event.ydata])
        
        for i, carga in enumerate(self.cargas):
            if i == self.carga_seleccionada_idx: continue
            if np.linalg.norm(carga['pos'] - nueva_pos) < 0.2: return 
                
        self.cargas[self.carga_seleccionada_idx]['pos'] = nueva_pos
        self.actualizar_grafica()

    def al_soltar_clic(self, event):
        self.carga_seleccionada_idx = None
        self.actualizar_grafica()

    def calcular_fuerza_entre_dos(self, q1, pos1, q2, pos2):
        r_vector = pos2 - pos1
        r_magnitud = np.linalg.norm(r_vector)
        if r_magnitud < 0.05: return np.array([0.0, 0.0])
        f_magnitud = K * (abs(q1 * q2) / (r_magnitud ** 2))
        r_unitario = r_vector / r_magnitud
        return f_magnitud * r_unitario if (q1 * q2 > 0) else -f_magnitud * r_unitario

    def actualizar_grafica(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        self.ax.clear()
        self.txt_resultados.delete("1.0", tk.END)
        
        if not self.cargas and not self.puntos_campo:
            self.ax.grid(True, linestyle='--')
            self.canvas.draw()
            return

        # PASO 4: Listado de cargas registradas
        self.txt_resultados.insert(tk.END, f"====== CARGAS EN EL SISTEMA ({len(self.cargas)}/{self.limite_cargas}) ======\n")
        for i, carga in enumerate(self.cargas):
            color = 'red' if carga['q'] > 0 else 'blue'
            self.ax.scatter(carga['pos'][0], carga['pos'][1], color=color, s=250, zorder=5)
            self.ax.text(carga['pos'][0]+0.15, carga['pos'][1]+0.15, f"q{i}", fontsize=10, fontweight='bold')
            self.txt_resultados.insert(tk.END, f"q{i}: {carga['q']*1e6:.1f} uC en ({carga['pos'][0]:.2f}, {carga['pos'][1]:.2f})m\n")

        # PASO 6: Análisis de Fuerzas y Distancias por Superposición
        idx_sel = self.combo_carga.current()
        if idx_sel != -1 and idx_sel < len(self.cargas) and len(self.cargas) > 1:
            f_neta = np.array([0.0, 0.0])
            carga_obj = self.cargas[idx_sel]
            self.txt_resultados.insert(tk.END, f"\n==== INTERACCIONES SOBRE LA CARGA q{idx_sel} ====\n")
            
            for i, carga in enumerate(self.cargas):
                if i == idx_sel: continue 
                
                # ¡NUEVO!: CÁLCULO DE LA DISTANCIA ESCALAR ANTES DE LA FUERZA REQUERIDO POR EL PDF
                dist = np.linalg.norm(carga_obj['pos'] - carga['pos'])
                
                # Calculamos las componentes vectoriales intermitentes de la fuerza parcial
                f_parcial = self.calcular_fuerza_entre_dos(carga['q'], carga['pos'], carga_obj['q'], carga_obj['pos'])
                f_neta += f_parcial  # Sumatoria del principio de superposición 
                
                # Imprimimos de forma secuencial la distancia y luego las componentes vectoriales resultantes
                self.txt_resultados.insert(tk.END, f"➔ Relación con Carga q{i}:\n")
                self.txt_resultados.insert(tk.END, f"  Distancia (r) = {dist:.4f} metros\n") 
                self.txt_resultados.insert(tk.END, f"  Componente Fx = {f_parcial[0]:.2e} N\n") 
                self.txt_resultados.insert(tk.END, f"  Componente Fy = {f_parcial[1]:.2e} N\n\n") 

            # Resultados globales finales sobre la carga seleccionada
            magnitud = np.linalg.norm(f_neta)
            angulo = np.degrees(np.arctan2(f_neta[1], f_neta[0]))
            self.txt_resultados.insert(tk.END, f"➔ VECTOR FUERZA NETA RESULTANTE:\n")
            self.txt_resultados.insert(tk.END, f"  Magnitud Total = {magnitud:.2e} N\n")
            self.txt_resultados.insert(tk.END, f"  Dirección (θ)  = {angulo:.1f}°\n")    

            if magnitud > 0:
                f_dir = f_neta / magnitud
                
                # Descomposición gráfica en componentes translúcidos para 2D
                if self.es_2d:
                    f_dir_x = np.array([f_neta[0] / magnitud, 0.0])
                    if np.linalg.norm(f_dir_x) > 0:
                        self.ax.quiver(carga_obj['pos'][0], carga_obj['pos'][1], f_dir_x[0], 0, 
                                       color='orange', scale=6, width=0.005, alpha=0.6)
                    
                    f_dir_y = np.array([0.0, f_neta[1] / magnitud])
                    if np.linalg.norm(f_dir_y) > 0:
                        self.ax.quiver(carga_obj['pos'][0], carga_obj['pos'][1], 0, f_dir_y[1], 
                                       color='deepskyblue', scale=6, width=0.005, alpha=0.6)

                # Vector de Fuerza Neta (Morado)
                self.ax.quiver(carga_obj['pos'][0], carga_obj['pos'][1], f_dir[0], f_dir[1] if self.es_2d else 0, 
                               color='purple', scale=6, width=0.008, zorder=6)

        # PASO 8: Cálculo del campo eléctrico total en los puntos definidos por el usuario
        self.txt_resultados.insert(tk.END, "\n==== CAMPO ELÉCTRICO EN PUNTOS DEL ESPACIO ====\n")
        for p in self.puntos_campo:
            e_total = np.array([0.0, 0.0])
            omitir = False
            for carga in self.cargas:
                r_vec = np.array(p) - carga['pos']
                r_mag = np.linalg.norm(r_vec)
                if r_mag < 0.1: 
                    omitir = True; break
                e_mag = K * abs(carga['q']) / (r_mag ** 2) 
                r_uni = r_vec / r_mag
                e_total += e_mag * r_uni if carga['q'] > 0 else -e_mag * r_uni 
            
            if not omitir and np.linalg.norm(e_total) > 0:
                e_mag_t = np.linalg.norm(e_total)
                # Formato del reporte de campo eléctrico
                self.txt_resultados.insert(tk.END, f"Punto {p}:\n  Ex: {e_total[0]:.2e} N/C\n  Ey: {e_total[1]:.2e} N/C\n  Magnitud: {e_mag_t:.2e} N/C\n\n")
                e_dir = e_total / e_mag_t
                # Pintar vectores de campo (Verde)
                self.ax.quiver(p[0], p[1], e_dir[0], e_dir[1] if self.es_2d else 0, color='green', scale=10, width=0.004)
                self.ax.scatter(p[0], p[1], color='green', marker='x', s=60)

        # Acondicionamiento de ejes y formato gráfico
        self.ax.axhline(0, color='black', linewidth=0.6)
        if self.es_2d:
            self.ax.axvline(0, color='black', linewidth=0.6)
            self.ax.set_ylabel("Posición Y (metros)")
        else:
            self.ax.get_yaxis().set_visible(False)
            
        self.ax.set_xlabel("Posición X (metros)")
        self.ax.set_title("Simulador Electrostático - Cargas, Fuerzas y Campos")
        self.ax.grid(True, linestyle='--')
        
        # Ajuste dinámico inteligente del zoom de los ejes según coordenadas tecleadas
        if xlim != (0.0, 1.0) or ylim != (0.0, 1.0): 
            self.ax.set_xlim(xlim)
            if self.es_2d: self.ax.set_ylim(ylim)
        else:
            todas_x = [c['pos'][0] for c in self.cargas] + [p[0] for p in self.puntos_campo]
            min_x, max_x = min(todas_x) - 3, max(todas_x) + 4
            self.ax.set_xlim([min_x, max_x])
            if self.es_2d:
                todas_y = [c['pos'][1] for c in self.cargas] + [p[1] for p in self.puntos_campo]
                min_y, max_y = min(todas_y) - 3, max(todas_y) + 4
                self.ax.set_ylim([min_y, max_y])
            
        self.canvas.draw()

# --- ARRANQUE NATIVO DE LA APLICACIÓN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaConfiguracion(root)
    root.mainloop()