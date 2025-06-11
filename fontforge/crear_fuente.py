import fontforge
import os
import csv

# Rutas a las carpetas
CARPETA_BASE = "plantilla"
RUTA_MAYUSCULAS = os.path.join(CARPETA_BASE, "mayusculas")
RUTA_MINUSCULAS = os.path.join(CARPETA_BASE, "minusculas")
RUTA_SIMBOLOS = os.path.join(CARPETA_BASE, "simbolos")
CSV_SIMBOLOS = os.path.join(RUTA_SIMBOLOS, "simbolos.csv")

# Crear nueva fuente
fuente = fontforge.font()
fuente.encoding = "UnicodeFull"
fuente.fontname = "MiFuente"
fuente.fullname = "Mi Fuente Personalizada"
fuente.familyname = "MiFuente"

def importar_glyph(nombre_archivo, caracter_unicode, ruta):
    ruta_completa = os.path.join(ruta, f"{nombre_archivo}.svg")
    if os.path.isfile(ruta_completa):
        print(f"Importando '{caracter_unicode}' desde {ruta_completa}")
        glyph = fuente.createChar(ord(caracter_unicode))
        glyph.importOutlines(ruta_completa)
        glyph.left_side_bearing = 50
        glyph.right_side_bearing = 50
        glyph.autoInstr()
    else:
        print(f"[!] Archivo no encontrado: {ruta_completa}")

# Importar mayúsculas
for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    importar_glyph(letra, letra, RUTA_MAYUSCULAS)

# Importar minúsculas
for letra in "abcdefghijklmnopqrstuvwxyz":
    importar_glyph(letra, letra, RUTA_MINUSCULAS)

# Importar símbolos desde CSV
if os.path.isfile(CSV_SIMBOLOS):
    with open(CSV_SIMBOLOS, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            nombre_archivo = fila['nombre'].strip()
            simbolo = fila['símbolo'].strip()
            if len(simbolo) == 1:
                importar_glyph(nombre_archivo, simbolo, RUTA_SIMBOLOS)
            else:
                print(f"[!] Símbolo inválido en CSV: {simbolo}")
else:
    print(f"[!] No se encontró el archivo CSV de símbolos: {CSV_SIMBOLOS}")

# Exportar fuente
fuente.generate("MiFuente.ttf")
fuente.save("MiFuente.sfd")
print("\n✅ Fuente generada correctamente: MiFuente.ttf")
