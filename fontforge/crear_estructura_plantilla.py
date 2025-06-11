import os

carpeta_base = "plantilla"
subcarpetas = ["mayusculas", "minusculas"]

for sub in subcarpetas:
    ruta = os.path.join(carpeta_base, sub)
    os.makedirs(ruta, exist_ok=True)

# Mayúsculas
for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    ruta_svg = os.path.join(carpeta_base, "mayusculas", f"{letra}.svg")
    with open(ruta_svg, "w", encoding="utf-8") as f:
        f.write("""<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>""")

# Minúsculas
for letra in "abcdefghijklmnopqrstuvwxyz":
    ruta_svg = os.path.join(carpeta_base, "minusculas", f"{letra}.svg")
    with open(ruta_svg, "w", encoding="utf-8") as f:
        f.write("""<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>""")

print("✅ Estructura de carpetas y archivos .svg vacíos creada.")
