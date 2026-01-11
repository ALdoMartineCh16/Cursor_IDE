def suma(a, b):
    """Realiza la suma de dos números"""
    return a + b

def resta(a, b):
    """Realiza la resta de dos números"""
    return a - b

def multiplicacion(a, b):
    """Realiza la multiplicación de dos números"""
    return a * b

def division(a, b):
    """Realiza la división de dos números"""
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

# Diccionario de operaciones
operaciones = {
    "suma": suma,
    "resta": resta,
    "multiplicación": multiplicacion,
    "multiplicacion": multiplicacion,  # También acepta sin tilde
    "división": division,
    "division": division,  # También acepta sin tilde
}

def main():
    """Función principal del programa"""
    print("=== Calculadora ===")
    print("Operaciones disponibles: suma, resta, multiplicación, división")
    print("Escribe 'salir' para terminar\n")
    
    while True:
        # Pedir operación al usuario
        operacion = input("Ingresa la operación (o 'salir' para terminar): ").strip().lower()
        
        # Verificar si el usuario quiere salir
        if operacion == "salir":
            print("¡Hasta luego!")
            break
        
        # Verificar si la operación es válida
        if operacion not in operaciones:
            print(f"Error: '{operacion}' no es una operación válida.")
            print("Operaciones disponibles: suma, resta, multiplicación, división\n")
            continue
        
        # Pedir los dos números
        try:
            num1 = float(input("Ingresa el primer número: "))
            num2 = float(input("Ingresa el segundo número: "))
        except ValueError:
            print("Error: Debes ingresar números válidos.\n")
            continue
        
        # Ejecutar la operación y mostrar el resultado
        try:
            resultado = operaciones[operacion](num1, num2)
            print(f"Resultado: {num1} {operacion} {num2} = {resultado}\n")
        except ValueError as e:
            print(f"Error: {e}\n")
        except Exception as e:
            print(f"Error inesperado: {e}\n")

if __name__ == "__main__":
    main()
