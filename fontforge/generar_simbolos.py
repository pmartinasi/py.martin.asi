import os
import csv

# Carpeta base para símbolos
carpeta_simbolos = os.path.join("plantilla", "simbolos")
os.makedirs(carpeta_simbolos, exist_ok=True)

# Lista de símbolos comunes
simbolos_comunes = [
    "!", "?", ".", ",", ":", ";", "-", "_", "+", "=",
    "*", "/", "\\", "(", ")", "[", "]", "{", "}",
    "@", "#", "$", "%", "&", "\"", "'", "<", ">", "|",
    "¡", "¿", "§", "°", "€", "¢", "¥"
]

# Ruta del CSV
csv_path = os.path.join(carpeta_simbolos, "simbolos.csv")

# Generar CSV y SVGs vacíos
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["nombre", "símbolo"])  # Encabezados

    for i, simbolo in enumerate(simbolos_comunes):
        nombre = str(i)
        writer.writerow([nombre, simbolo])

        # Crear SVG vacío
        ruta_svg = os.path.join(carpeta_simbolos, f"{nombre}.svg")
        with open(ruta_svg, "w", encoding="utf-8") as f:
            f.write("""<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>""")

print(f"✅ {len(simbolos_comunes)} símbolos creados con CSV en: {csv_path}")
