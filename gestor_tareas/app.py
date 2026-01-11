from flask import Flask, request, redirect, render_template
import json
import os

app = Flask(__name__)

# Nombre del archivo de persistencia
ARCHIVO_TAREAS = 'tareas.json'

# Lista global de tareas
tareas = []
# Contador para IDs incrementales
contador_id = 1

def cargar_datos():
    """
    Carga las tareas y el contador desde el archivo JSON.
    Si el archivo no existe o hay errores, inicia con valores por defecto.
    """
    global contador_id, tareas
    
    try:
        if os.path.exists(ARCHIVO_TAREAS):
            with open(ARCHIVO_TAREAS, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Validar estructura de datos
                if isinstance(data, dict) and 'tareas' in data and 'contador_id' in data:
                    tareas = data['tareas']
                    contador_id = data['contador_id']
                    
                    # Validar que tareas sea una lista
                    if not isinstance(tareas, list):
                        tareas = []
                    
                    # Validar que contador_id sea un entero válido
                    if not isinstance(contador_id, int) or contador_id < 1:
                        # Si hay tareas, calcular el siguiente ID basado en el máximo
                        contador_id = max([t['id'] for t in tareas], default=0) + 1
                else:
                    # Estructura inválida, reiniciar
                    tareas = []
                    contador_id = 1
    except (json.JSONDecodeError, IOError, ValueError) as e:
        # Si hay error al leer el archivo, iniciar con valores por defecto
        print(f"Error al cargar datos: {e}. Iniciando con valores por defecto.")
        tareas = []
        contador_id = 1

def guardar_datos():
    """
    Guarda las tareas y el contador en el archivo JSON.
    Maneja errores de escritura de forma segura.
    """
    try:
        data = {
            'contador_id': contador_id,
            'tareas': tareas
        }
        
        # Escribir a un archivo temporal primero, luego renombrar (más seguro)
        temp_file = ARCHIVO_TAREAS + '.tmp'
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Reemplazar el archivo original con el temporal
        if os.path.exists(ARCHIVO_TAREAS):
            os.replace(temp_file, ARCHIVO_TAREAS)
        else:
            os.rename(temp_file, ARCHIVO_TAREAS)
            
    except (IOError, OSError) as e:
        print(f"Error al guardar datos: {e}")
        # Intentar eliminar archivo temporal si existe
        try:
            if os.path.exists(ARCHIVO_TAREAS + '.tmp'):
                os.remove(ARCHIVO_TAREAS + '.tmp')
        except:
            pass

def agregar_tarea(texto):
    """
    Agrega una nueva tarea a la lista global.
    
    Args:
        texto (str): El texto de la tarea a agregar
    
    Returns:
        int: El ID de la tarea creada
    """
    global contador_id, tareas
    
    nueva_tarea = {
        'id': contador_id,
        'texto': texto,
        'hecho': False
    }
    
    tareas.append(nueva_tarea)
    contador_id += 1
    guardar_datos()  # Guardar después de agregar
    
    return nueva_tarea['id']

def completar_tarea(id):
    """
    Marca una tarea como completada.
    
    Args:
        id (int): El ID de la tarea a completar
    
    Returns:
        bool: True si la tarea fue encontrada y marcada, False si no existe
    """
    global tareas
    
    for tarea in tareas:
        if tarea['id'] == id:
            tarea['hecho'] = True
            guardar_datos()  # Guardar después de completar
            return True
    
    return False

def eliminar_tarea(id):
    """
    Elimina una tarea de la lista global.
    
    Args:
        id (int): El ID de la tarea a eliminar
    
    Returns:
        bool: True si la tarea fue encontrada y eliminada, False si no existe
    """
    global tareas
    
    for i, tarea in enumerate(tareas):
        if tarea['id'] == id:
            tareas.pop(i)
            guardar_datos()  # Guardar después de eliminar
            return True
    
    return False

def editar_tarea(id, nuevo_texto):
    """
    Edita el texto de una tarea.
    
    Args:
        id (int): El ID de la tarea a editar
        nuevo_texto (str): El nuevo texto de la tarea
    
    Returns:
        bool: True si la tarea fue encontrada y editada, False si no existe
    """
    global tareas
    
    for tarea in tareas:
        if tarea['id'] == id:
            tarea['texto'] = nuevo_texto
            guardar_datos()  # Guardar después de editar
            return True
    
    return False

# Cargar datos al iniciar la aplicación
cargar_datos()

@app.route('/')
def index():
    # Ordenar tareas: incompletas primero, luego completadas
    tareas_ordenadas = sorted(tareas, key=lambda t: t['hecho'])
    return render_template('index.html', tareas=tareas_ordenadas)

@app.route('/agregar', methods=['POST'])
def agregar():
    texto_tarea = request.form.get('texto_tarea')
    if texto_tarea:
        agregar_tarea(texto_tarea)
    return redirect('/')

@app.route('/completar/<int:id>')
def completar(id):
    completar_tarea(id)
    return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    eliminar_tarea(id)
    return redirect('/')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        nuevo_texto = request.form.get('texto_tarea')
        if nuevo_texto:
            editar_tarea(id, nuevo_texto)
        return redirect('/')
    else:
        # Buscar la tarea para mostrar el formulario
        tarea = None
        for t in tareas:
            if t['id'] == id:
                tarea = t
                break
        
        if not tarea:
            return redirect('/')
        
        return render_template('editar.html', tarea=tarea)


if __name__ == '__main__':
    app.run(debug=True)