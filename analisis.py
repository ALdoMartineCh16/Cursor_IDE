import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('datos.csv')

# Calcular estadísticas para cada columna
print("=== Estadísticas descriptivas ===\n")

for columna in df.columns:
    media = df[columna].mean()
    mediana = df[columna].median()
    desviacion = df[columna].std()
    
    print(f"Columna: {columna}")
    print(f"  Media: {media:.2f}")
    print(f"  Mediana: {mediana:.2f}")
    print(f"  Desviación estándar: {desviacion:.2f}")
    print()

# Crear gráfico de dispersión
plt.figure(figsize=(8, 6))
plt.scatter(df['Numero1'], df['Numero2'], alpha=0.6, s=50)
plt.xlabel('Numero1')
plt.ylabel('Numero2')
plt.title('Gráfico de Dispersión: Numero1 vs Numero2')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Mostrar el gráfico
plt.show()
