print("Hello, Cursor!")

# Este bucle imprime los números del 0 al 4 en la consola
for i in range(5):
    print(i)

# ===========================================
# EJEMPLOS DE CÓMO ABRIR Y LEER ARCHIVOS
# ===========================================

# 1. MÉTODO BÁSICO (necesitas cerrar el archivo manualmente)
archivo = open("ejemplo.txt", "r", encoding="utf-8")
contenido = archivo.read()  # Lee todo el contenido
archivo.close()

# 2. MÉTODO RECOMENDADO: Context Manager (cierra automáticamente)
with open("ejemplo.txt", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()  # Lee todo el contenido como una cadena
    print(contenido)

# 3. Leer línea por línea (método recomendado para archivos grandes)
with open("ejemplo.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        print(linea.strip())  # strip() elimina los saltos de línea

# 4. Leer todas las líneas como una lista
with open("ejemplo.txt", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()  # Devuelve una lista con todas las líneas
    for linea in lineas:
        print(linea.strip())

# 5. Leer una sola línea
with open("ejemplo.txt", "r", encoding="utf-8") as archivo:
    primera_linea = archivo.readline()  # Lee solo la primera línea
    print(primera_linea)

# 6. Leer un número específico de caracteres
with open("ejemplo.txt", "r", encoding="utf-8") as archivo:
    primeros_100_caracteres = archivo.read(100)  # Lee solo los primeros 100 caracteres
    print(primeros_100_caracteres)

# NOTA: 
# - "r" significa modo lectura (read)
# - encoding="utf-8" es importante para caracteres especiales y acentos
# - Siempre usa "with" para asegurar que el archivo se cierre correctamente