# 📝 Gestor de Tareas

Una aplicación web moderna y elegante para gestionar tus tareas diarias. Desarrollada con Flask y Python, permite agregar, editar, completar y eliminar tareas de manera intuitiva.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Características

- ✅ **Agregar tareas**: Crea nuevas tareas con un simple formulario
- 📝 **Editar tareas**: Modifica el texto de cualquier tarea existente
- ✓ **Completar tareas**: Marca las tareas como completadas
- 🗑️ **Eliminar tareas**: Elimina tareas que ya no necesitas
- 💾 **Persistencia de datos**: Las tareas se guardan automáticamente en un archivo JSON
- 🎨 **Interfaz moderna**: Diseño atractivo con gradientes y animaciones suaves
- 📱 **Responsive**: Se adapta a diferentes tamaños de pantalla

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.7+
- **Framework Web**: Flask
- **Frontend**: HTML5, CSS3
- **Persistencia**: JSON (archivo local)

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

1. **Clona el repositorio** (o descarga los archivos):
```bash
git clone https://github.com/tu-usuario/gestor-tareas.git
cd gestor-tareas
```

2. **Crea un entorno virtual** (recomendado):
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instala las dependencias**:
```bash
pip install flask
```

O crea un archivo `requirements.txt` con:
```
Flask>=2.0.0
```

Y luego ejecuta:
```bash
pip install -r requirements.txt
```

## 📖 Uso

1. **Inicia el servidor Flask**:
```bash
python app.py
```

2. **Abre tu navegador** y visita:
```
http://127.0.0.1:5000
```

3. **¡Comienza a gestionar tus tareas!**
   - Escribe una nueva tarea en el campo de texto y haz clic en "Agregar"
   - Haz clic en "Completar" para marcar una tarea como terminada
   - Haz clic en "Editar" para modificar el texto de una tarea
   - Haz clic en "Eliminar" para borrar una tarea (con confirmación)

## 📁 Estructura del Proyecto

```
gestor_tareas/
│
├── app.py                 # Aplicación principal Flask
├── tareas.json            # Archivo de persistencia (se crea automáticamente)
├── README.md              # Este archivo
├── requirements.txt       # Dependencias del proyecto
└── templates/             # Plantillas HTML
    ├── index.html         # Página principal
    └── editar.html        # Página de edición de tareas
```

## 💾 Persistencia de Datos

Las tareas se guardan automáticamente en el archivo `tareas.json` en formato JSON. Este archivo se crea automáticamente la primera vez que agregas una tarea. Los datos se guardan después de cada operación (agregar, editar, completar, eliminar).

El formato del archivo JSON es:
```json
{
  "contador_id": 3,
  "tareas": [
    {
      "id": 1,
      "texto": "Mi primera tarea",
      "hecho": false
    },
    {
      "id": 2,
      "texto": "Segunda tarea completada",
      "hecho": true
    }
  ]
}
```

## 🔧 Funcionalidades Técnicas

- **IDs incrementales**: Cada tarea recibe un ID único que se incrementa automáticamente
- **Ordenamiento inteligente**: Las tareas incompletas se muestran primero, seguidas de las completadas
- **Validación de datos**: El sistema valida la estructura de datos al cargar
- **Escritura atómica**: Los datos se escriben de forma segura usando archivos temporales
- **Manejo de errores**: Gestión robusta de errores en operaciones de lectura/escritura

## 🎨 Personalización

Puedes personalizar fácilmente la aplicación modificando:

- **Estilos CSS**: Edita los estilos en los archivos HTML dentro de las etiquetas `<style>`
- **Colores del tema**: Cambia los gradientes y colores en las clases CSS
- **Texto**: Modifica los textos y mensajes en las plantillas HTML

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto:

1. Haz un Fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Puedes usar, modificar y distribuir este código libremente.

## 👤 Autor

Creado con ❤️ para gestionar tareas de manera eficiente.

## 🔮 Posibles Mejoras Futuras

- [ ] Categorías o etiquetas para las tareas
- [ ] Fechas de vencimiento
- [ ] Búsqueda y filtrado de tareas
- [ ] Exportar/importar tareas
- [ ] Modo oscuro
- [ ] Notificaciones
- [ ] Autenticación de usuarios
- [ ] Base de datos en lugar de JSON

## 📞 Soporte

Si encuentras algún problema o tienes preguntas, por favor abre un [issue](https://github.com/tu-usuario/gestor-tareas/issues) en el repositorio.

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!
