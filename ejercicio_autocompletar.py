# Crear una lista con los cuadrados de los n primeros números naturales
def cuadrados(n):
    return [i**2 for i in range(1, n+1)]

# print(cuadrados(10))  # Comentado para ejecutar solo las pruebas

def numero_primo(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Solo verificamos hasta √n, ya que si hay un divisor mayor que √n,
    # también hay uno menor que √n
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Función de prueba para casos de programación competitiva
def test_numero_primo():
    casos_prueba = [
        # Casos límite
        (0, False, "Caso límite: 0 (no es primo)"),
        (1, False, "Caso límite: 1 (no es primo)"),
        (2, True, "Caso límite: 2 (único primo par)"),
        
        # Números pequeños primos
        (3, True, "Primo pequeño: 3"),
        (5, True, "Primo pequeño: 5"),
        (7, True, "Primo pequeño: 7"),
        (11, True, "Primo pequeño: 11"),
        (13, True, "Primo pequeño: 13"),
        (17, True, "Primo pequeño: 17"),
        (19, True, "Primo pequeño: 19"),
        (23, True, "Primo pequeño: 23"),
        (29, True, "Primo pequeño: 29"),
        
        # Números pequeños compuestos
        (4, False, "Compuesto: 4 = 2²"),
        (6, False, "Compuesto: 6 = 2×3"),
        (8, False, "Compuesto: 8 = 2³"),
        (9, False, "Compuesto: 9 = 3²"),
        (10, False, "Compuesto: 10 = 2×5"),
        (12, False, "Compuesto: 12 = 2²×3"),
        (15, False, "Compuesto: 15 = 3×5"),
        (21, False, "Compuesto: 21 = 3×7"),
        (25, False, "Compuesto: 25 = 5²"),
        (27, False, "Compuesto: 27 = 3³"),
        
        # Cuadrados perfectos (nunca son primos excepto casos especiales)
        (16, False, "Cuadrado perfecto: 16 = 4²"),
        (49, False, "Cuadrado perfecto: 49 = 7²"),
        (121, False, "Cuadrado perfecto: 121 = 11²"),
        
        # Primos medianos
        (97, True, "Primo mediano: 97"),
        (101, True, "Primo mediano: 101"),
        (103, True, "Primo mediano: 103"),
        (107, True, "Primo mediano: 107"),
        (109, True, "Primo mediano: 109"),
        (113, True, "Primo mediano: 113"),
        (127, True, "Primo mediano: 127"),
        (131, True, "Primo mediano: 131"),
        (137, True, "Primo mediano: 137"),
        (139, True, "Primo mediano: 139"),
        (149, True, "Primo mediano: 149"),
        (151, True, "Primo mediano: 151"),
        
        # Compuestos medianos
        (100, False, "Compuesto: 100 = 2²×5²"),
        (102, False, "Compuesto: 102 = 2×3×17"),
        (105, False, "Compuesto: 105 = 3×5×7"),
        (143, False, "Compuesto: 143 = 11×13"),
        (169, False, "Compuesto: 169 = 13²"),
        (187, False, "Compuesto: 187 = 11×17"),
        
        # Primos grandes (típicos en programación competitiva)
        (997, True, "Primo grande: 997"),
        (1009, True, "Primo grande: 1009"),
        (1013, True, "Primo grande: 1013"),
        (1019, True, "Primo grande: 1019"),
        (1021, True, "Primo grande: 1021"),
        (10007, True, "Primo muy grande: 10007"),
        (10009, True, "Primo muy grande: 10009"),
        (99991, True, "Primo muy grande: 99991"),
        
        # Compuestos grandes
        (9999, False, "Compuesto grande: 9999 = 9×1111"),
        (10000, False, "Compuesto grande: 10000 = 2⁴×5⁴"),
        (10001, False, "Compuesto grande: 10001 = 73×137"),
        (99999, False, "Compuesto grande: 99999 = 9×11111"),
        
        # Casos especiales: números cerca de cuadrados perfectos
        (1681, False, "Cuadrado perfecto: 1681 = 41²"),
        (2209, False, "Cuadrado perfecto: 2209 = 47²"),
        (3481, False, "Cuadrado perfecto: 3481 = 59²"),
        
        # Primos gemelos (primos que difieren en 2)
        (41, True, "Primo gemelo: 41"),
        (43, True, "Primo gemelo: 43"),
        (59, True, "Primo gemelo: 59"),
        (61, True, "Primo gemelo: 61"),
        (71, True, "Primo gemelo: 71"),
        (73, True, "Primo gemelo: 73"),
    ]
    
    print("=" * 60)
    print("CASOS DE PRUEBA - FUNCIÓN numero_primo()")
    print("=" * 60)
    print()
    
    pasados = 0
    fallidos = 0
    
    for numero, esperado, descripcion in casos_prueba:
        resultado = numero_primo(numero)
        estado = "✓ PASS" if resultado == esperado else "✗ FAIL"
        
        esperado_str = str(esperado)
        resultado_str = str(resultado)
        
        if resultado == esperado:
            pasados += 1
            print(f"{estado} | n={numero:6d} | Esperado: {esperado_str:5s} | Obtenido: {resultado_str:5s} | {descripcion}")
        else:
            fallidos += 1
            print(f"{estado} | n={numero:6d} | Esperado: {esperado_str:5s} | Obtenido: {resultado_str:5s} | {descripcion}")
    
    print()
    print("=" * 60)
    print(f"RESUMEN: {pasados} casos pasados, {fallidos} casos fallidos")
    print(f"Total: {pasados + fallidos} casos de prueba")
    print("=" * 60)
    
    return fallidos == 0

# Ejecutar las pruebas
if __name__ == "__main__":
    test_numero_primo()
    
    # También puedes probar manualmente:
    # n = int(input("\nIngresa un número para probar: "))
    # print(f"¿Es {n} primo? {numero_primo(n)}")
