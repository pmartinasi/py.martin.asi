import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Inicialización del modelo BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Pedir al usuario la carpeta con imágenes
entrada_usuario = input("📁 Introduce la ruta de la carpeta con imágenes (deja vacío para usar './imagenes'): ").strip()
carpeta_imagenes = entrada_usuario if entrada_usuario else "./imagenes"

# Comprobar que la carpeta existe
if not os.path.isdir(carpeta_imagenes):
    print(f"❌ La carpeta '{carpeta_imagenes}' no existe.")
    exit()

# Crear carpeta de salida
carpeta_salida = carpeta_imagenes
os.makedirs(carpeta_salida, exist_ok=True)

def generar_metatags(texto):
    palabras = texto.lower().replace(".", "").replace(",", "").split()
    metatags = list(set([p for p in palabras if len(p) > 3]))
    return metatags[:10]  # Máximo 10 metatags

# Procesar imágenes
for archivo in os.listdir(carpeta_imagenes):
    if archivo.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        ruta_imagen = os.path.join(carpeta_imagenes, archivo)
        imagen = Image.open(ruta_imagen).convert('RGB')

        # Generar descripción
        inputs = processor(images=imagen, return_tensors="pt")
        out = model.generate(**inputs)
        descripcion = processor.decode(out[0], skip_special_tokens=True)

        # Generar metatags
        metatags = generar_metatags(descripcion)

        # Guardar archivo TXT
        nombre_base = os.path.splitext(archivo)[0]
        ruta_txt = os.path.join(carpeta_salida, f"{nombre_base}.txt")

        with open(ruta_txt, "w", encoding="utf-8") as f:
            f.write(f"Archivo: {archivo}\n")
            f.write(f"Descripción: {descripcion}\n")
            f.write(f"Metatags: {', '.join(metatags)}\n")

        print(f"✓ Procesado: {archivo} → {nombre_base}.txt")

print(f"\n✅ Todos los archivos .txt se han generado en: {carpeta_salida}")
