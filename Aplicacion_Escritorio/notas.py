#!/usr/bin/env python3
"""
Editor de Notas Avanzado
Versión 2.0 - Con todas las funcionalidades mejoradas

Características:
- Guardar y Guardar como... separados
- Detección de cambios y diálogo al salir
- Menú Editar con cortar, copiar, pegar
- Numeración de líneas
- Cambio de fuente y tamaño
- Scrollbars
- Atajos de teclado
- Internacionalización (español)
"""

import tkinter as tk
from tkinter import filedialog, messagebox, font, scrolledtext
from tkinter import ttk
import os


class EditorNotas(tk.Tk):

    def __init__(self):
        super().__init__()

        # Variables de estado
        self.archivo_actual = None
        self.cambios_sin_guardar = False
        self.fuente_actual = ("Consolas", 10)  # Fuente por defecto

        # Configuración de la ventana
        self.title("Editor de Notas - Sin título")
        self.geometry("800x600")
        self.minsize(400, 300)

        # Configurar protocolo de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        # Crear interfaz
        self.crear_widgets()
        self.crear_menu()
        self.crear_atajos_teclado()
        self.actualizar_numeracion_lineas()

        # Vincular eventos de cambio de texto
        self.text_area.bind("<<Modified>>", self.on_texto_modificado)
        self.text_area.bind("<KeyRelease>", lambda e: self.actualizar_numeracion_lineas())
        self.text_area.bind("<ButtonRelease>", lambda e: self.actualizar_numeracion_lineas())

    def crear_widgets(self):
        """Crear todos los widgets de la interfaz"""

        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para numeración de líneas
        self.line_numbers_frame = ttk.Frame(main_frame, width=40)
        self.line_numbers_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Canvas para numeración de líneas
        self.line_numbers_canvas = tk.Canvas(
            self.line_numbers_frame,
            width=35,
            bg="#f0f0f0",
            highlightthickness=0
        )
        self.line_numbers_canvas.pack(fill=tk.BOTH, expand=True)

        # Área de texto con scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(text_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Área de texto
        self.text_area = tk.Text(
            text_frame,
            wrap=tk.NONE,  # No wrap automático
            undo=True,     # Soporte para deshacer/rehacer
            font=self.fuente_actual,
            padx=5,
            pady=5
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Configurar scrollbars
        self.text_area.config(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        scrollbar_y.config(command=self.text_area.yview)
        scrollbar_x.config(command=self.text_area.xview)

        # Vincular scroll del canvas de numeración con el texto
        self.text_area.bind("<MouseWheel>", self.on_scroll_mouse)
        scrollbar_y.bind("<MouseWheel>", self.on_scroll_mouse)

    def crear_menu(self):
        """Crear la barra de menú completa"""

        menubar = tk.Menu(self)

        # ===== MENÚ ARCHIVO =====
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Nuevo", command=self.nuevo_archivo, accelerator="Ctrl+N")
        filemenu.add_command(label="Abrir...", command=self.abrir_archivo, accelerator="Ctrl+O")
        filemenu.add_separator()
        filemenu.add_command(label="Guardar", command=self.guardar_archivo, accelerator="Ctrl+S")
        filemenu.add_command(label="Guardar como...", command=self.guardar_como, accelerator="Ctrl+Shift+S")
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.cerrar_aplicacion, accelerator="Ctrl+Q")
        menubar.add_cascade(label="Archivo", menu=filemenu)

        # ===== MENÚ EDITAR =====
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Deshacer", command=self.deshacer, accelerator="Ctrl+Z")
        editmenu.add_command(label="Rehacer", command=self.rehacer, accelerator="Ctrl+Y")
        editmenu.add_separator()
        editmenu.add_command(label="Cortar", command=self.cortar, accelerator="Ctrl+X")
        editmenu.add_command(label="Copiar", command=self.copiar, accelerator="Ctrl+C")
        editmenu.add_command(label="Pegar", command=self.pegar, accelerator="Ctrl+V")
        editmenu.add_separator()
        editmenu.add_command(label="Seleccionar todo", command=self.seleccionar_todo, accelerator="Ctrl+A")
        editmenu.add_command(label="Eliminar línea", command=self.eliminar_linea, accelerator="Ctrl+L")
        menubar.add_cascade(label="Editar", menu=editmenu)

        # ===== MENÚ VER =====
        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_checkbutton(label="Numeración de líneas", command=self.toggle_numeracion_lineas,
                                variable=tk.BooleanVar(value=True))
        viewmenu.add_separator()
        viewmenu.add_command(label="Cambiar fuente...", command=self.cambiar_fuente)
        menubar.add_cascade(label="Ver", menu=viewmenu)

        # ===== MENÚ AYUDA =====
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Acerca de", command=self.acerca_de)
        helpmenu.add_command(label="Atajos de teclado", command=self.mostrar_atajos)
        menubar.add_cascade(label="Ayuda", menu=helpmenu)

        self.config(menu=menubar)

    def crear_atajos_teclado(self):
        """Configurar atajos de teclado"""

        # Archivo
        self.bind("<Control-n>", lambda e: self.nuevo_archivo())
        self.bind("<Control-o>", lambda e: self.abrir_archivo())
        self.bind("<Control-s>", lambda e: self.guardar_archivo())
        self.bind("<Control-Shift-S>", lambda e: self.guardar_como())
        self.bind("<Control-q>", lambda e: self.cerrar_aplicacion())

        # Editar
        self.bind("<Control-z>", lambda e: self.deshacer())
        self.bind("<Control-y>", lambda e: self.rehacer())
        self.bind("<Control-x>", lambda e: self.cortar())
        self.bind("<Control-c>", lambda e: self.copiar())
        self.bind("<Control-v>", lambda e: self.pegar())
        self.bind("<Control-a>", lambda e: self.seleccionar_todo())
        self.bind("<Control-l>", lambda e: self.eliminar_linea())

        # Funciones adicionales
        self.bind("<F1>", lambda e: self.mostrar_atajos())

    # ===== FUNCIONES DE ARCHIVO =====

    def nuevo_archivo(self):
        """Crear un nuevo archivo"""
        if self.confirmar_guardar_cambios():
            self.text_area.delete(1.0, tk.END)
            self.archivo_actual = None
            self.cambios_sin_guardar = False
            self.title("Editor de Notas - Sin título")
            self.actualizar_numeracion_lineas()

    def abrir_archivo(self):
        """Abrir un archivo existente"""
        if not self.confirmar_guardar_cambios():
            return

        filepath = filedialog.askopenfilename(
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Archivos Python", "*.py"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                contenido = file.read()

            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, contenido)
            self.archivo_actual = filepath
            self.cambios_sin_guardar = False
            self.title(f"Editor de Notas - {os.path.basename(filepath)}")
            self.actualizar_numeracion_lineas()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def guardar_archivo(self):
        """Guardar el archivo actual"""
        if self.archivo_actual:
            self._guardar_archivo(self.archivo_actual)
        else:
            self.guardar_como()

    def guardar_como(self):
        """Guardar con nombre de archivo diferente"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Archivos Python", "*.py"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not filepath:
            return

        if self._guardar_archivo(filepath):
            self.archivo_actual = filepath
            self.title(f"Editor de Notas - {os.path.basename(filepath)}")

    def _guardar_archivo(self, filepath):
        """Función interna para guardar archivo"""
        try:
            contenido = self.text_area.get(1.0, tk.END)
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(contenido.rstrip() + "\n")  # Asegurar nueva línea al final

            self.cambios_sin_guardar = False
            return True

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
            return False

    def cerrar_aplicacion(self):
        """Cerrar la aplicación con confirmación si hay cambios"""
        if self.confirmar_guardar_cambios():
            self.quit()

    def confirmar_guardar_cambios(self):
        """Preguntar al usuario si quiere guardar cambios pendientes"""
        if not self.cambios_sin_guardar:
            return True

        respuesta = messagebox.askyesnocancel(
            "Guardar cambios",
            "¿Desea guardar los cambios antes de continuar?",
            icon="warning"
        )

        if respuesta is None:  # Cancelar
            return False
        elif respuesta:  # Sí, guardar
            return self.guardar_archivo()  # Retorna True si se guardó correctamente
        else:  # No, no guardar
            return True

    # ===== FUNCIONES DE EDICIÓN =====

    def deshacer(self):
        """Deshacer la última acción"""
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass  # No hay más acciones para deshacer

    def rehacer(self):
        """Rehacer la última acción deshecha"""
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass  # No hay más acciones para rehacer

    def cortar(self):
        """Cortar texto seleccionado"""
        try:
            self.text_area.event_generate("<<Cut>>")
        except:
            pass

    def copiar(self):
        """Copiar texto seleccionado"""
        try:
            self.text_area.event_generate("<<Copy>>")
        except:
            pass

    def pegar(self):
        """Pegar desde el portapapeles"""
        try:
            self.text_area.event_generate("<<Paste>>")
        except:
            pass

    def seleccionar_todo(self):
        """Seleccionar todo el texto"""
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, tk.END)
        self.text_area.focus()

    def eliminar_linea(self):
        """Eliminar la línea actual"""
        try:
            # Obtener línea actual
            linea_actual = self.text_area.index(tk.INSERT).split(".")[0]

            # Seleccionar la línea completa
            inicio_linea = f"{linea_actual}.0"
            fin_linea = f"{linea_actual}.end"

            # Si la línea no está vacía, eliminarla
            if self.text_area.get(inicio_linea, fin_linea).strip():
                self.text_area.delete(inicio_linea, f"{linea_actual}.end+1c")
            else:
                # Si está vacía, eliminar solo el carácter de nueva línea
                self.text_area.delete(inicio_linea, fin_linea + "+1c")

        except:
            pass

    # ===== FUNCIONES DE VISUALIZACIÓN =====

    def on_texto_modificado(self, event=None):
        """Se llama cuando el texto es modificado"""
        if hasattr(self, 'text_area'):
            self.cambios_sin_guardar = True
            self.text_area.edit_modified(False)  # Resetear el flag de modificación

    def on_scroll_mouse(self, event):
        """Manejar scroll del mouse en el área de numeración"""
        self.text_area.yview_scroll(int(-1*(event.delta/120)), "units")
        self.actualizar_numeracion_lineas()

    def actualizar_numeracion_lineas(self):
        """Actualizar la numeración de líneas"""
        if not hasattr(self, 'line_numbers_canvas'):
            return

        self.line_numbers_canvas.delete("all")

        # Obtener información del texto
        texto = self.text_area.get("1.0", tk.END)
        lineas = texto.split("\n")

        if texto.endswith("\n"):
            lineas = lineas[:-1]  # No contar línea vacía al final

        # Obtener la primera línea visible
        primera_linea_visible = int(self.text_area.index("@0,0").split(".")[0])

        # Dibujar números de línea
        y = 5  # Margen superior
        line_height = 16  # Altura aproximada de línea (basado en fuente Consolas 10)

        for i in range(len(lineas)):
            numero_linea = i + 1

            # Solo mostrar líneas cercanas a la visible para rendimiento
            if abs(numero_linea - primera_linea_visible) < 50:
                color = "#666666" if numero_linea == primera_linea_visible else "#999999"
                self.line_numbers_canvas.create_text(
                    30, y, text=str(numero_linea),
                    anchor="e", font=("Consolas", 9), fill=color
                )

            y += line_height

    def toggle_numeracion_lineas(self):
        """Mostrar/ocultar numeración de líneas"""
        if self.line_numbers_frame.winfo_ismapped():
            self.line_numbers_frame.pack_forget()
        else:
            self.line_numbers_frame.pack(side=tk.LEFT, fill=tk.Y)

    def cambiar_fuente(self):
        """Abrir diálogo para cambiar fuente y tamaño"""
        # Crear ventana de diálogo
        dialog = tk.Toplevel(self)
        dialog.title("Cambiar fuente")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Frame principal
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Selector de fuente
        ttk.Label(frame, text="Fuente:").grid(row=0, column=0, sticky=tk.W, pady=2)
        fuente_var = tk.StringVar(value=self.fuente_actual[0])
        fuente_combo = ttk.Combobox(frame, textvariable=fuente_var, state="readonly")
        fuente_combo['values'] = ["Consolas", "Courier New", "Arial", "Times New Roman", "Verdana"]
        fuente_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        # Selector de tamaño
        ttk.Label(frame, text="Tamaño:").grid(row=1, column=0, sticky=tk.W, pady=2)
        tamano_var = tk.IntVar(value=self.fuente_actual[1])
        tamano_spin = tk.Spinbox(frame, from_=8, to=24, textvariable=tamano_var, width=5)
        tamano_spin.grid(row=1, column=1, sticky=tk.W, pady=2)

        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        def aplicar_cambios():
            nueva_fuente = (fuente_var.get(), tamano_var.get())
            self.fuente_actual = nueva_fuente
            self.text_area.config(font=nueva_fuente)
            self.actualizar_numeracion_lineas()
            dialog.destroy()

        ttk.Button(button_frame, text="Aplicar", command=aplicar_cambios).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.RIGHT)

        # Centrar diálogo
        dialog.geometry(f"+{self.winfo_x() + 50}+{self.winfo_y() + 50}")

    # ===== FUNCIONES DE AYUDA =====

    def acerca_de(self):
        """Mostrar información sobre la aplicación"""
        messagebox.showinfo(
            "Acerca de Editor de Notas",
            "Editor de Notas Avanzado v2.0\n\n"
            "Características:\n"
            "• Guardar y Guardar como...\n"
            "• Detección de cambios\n"
            "• Menú Editar completo\n"
            "• Numeración de líneas\n"
            "• Cambio de fuente\n"
            "• Atajos de teclado\n\n"
            "Creado con Tkinter y Python"
        )

    def mostrar_atajos(self):
        """Mostrar ventana con atajos de teclado"""
        atajos = tk.Toplevel(self)
        atajos.title("Atajos de Teclado")
        atajos.geometry("400x500")
        atajos.resizable(False, False)
        atajos.transient(self)

        # Frame con scrollbar
        frame = ttk.Frame(atajos, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(frame, text="Atajos de Teclado", font=("", 12, "bold")).pack(pady=(0, 10))

        # Crear text widget para mostrar atajos
        text_atajos = tk.Text(frame, wrap=tk.WORD, height=20, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(frame, command=text_atajos.yview)
        text_atajos.config(yscrollcommand=scrollbar.set)

        text_atajos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Contenido de atajos
        contenido = """ARCHIVO:
• Ctrl+N: Nuevo archivo
• Ctrl+O: Abrir archivo
• Ctrl+S: Guardar
• Ctrl+Shift+S: Guardar como...
• Ctrl+Q: Salir

EDITAR:
• Ctrl+Z: Deshacer
• Ctrl+Y: Rehacer
• Ctrl+X: Cortar
• Ctrl+C: Copiar
• Ctrl+V: Pegar
• Ctrl+A: Seleccionar todo
• Ctrl+L: Eliminar línea

OTROS:
• F1: Mostrar esta ayuda
• Mouse wheel: Scroll"""

        text_atajos.insert(tk.END, contenido)
        text_atajos.config(state=tk.DISABLED)  # Solo lectura

        # Botón cerrar
        ttk.Button(frame, text="Cerrar", command=atajos.destroy).pack(pady=10)

        # Centrar ventana
        atajos.geometry(f"+{self.winfo_x() + 100}+{self.winfo_y() + 50}")


if __name__ == "__main__":
    app = EditorNotas()
    app.mainloop()