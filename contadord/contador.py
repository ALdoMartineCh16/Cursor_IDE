# 1. Pedir al usuario la ruta de un archivo de texto.
archivo = input("Ingrese la ruta del archivo de texto: ")
try:
    with open(archivo, "r", encoding="utf-8") as f:
        texto = f.read()
except FileNotFoundError:
    print("El archivo especificado no existe")
    exit(1)

import re
palabras = re.findall(r"\w+", texto.lower())
total_palabras = len(palabras)
print(f"Total de palabras: {total_palabras}")