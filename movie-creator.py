import os
import random
import cv2
import numpy as np
import tempfile
from shutil import rmtree
import subprocess

# Funciones de transiciones
def fade_transition(img1, img2, frames=30):
    """ Realiza una transición suave de fundido entre dos imágenes """
    height, width, _ = img1.shape
    transition = []
    for i in range(frames):
        alpha = i / frames
        blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
        transition.append(blended)
    return transition

def zoom_transition(img1, img2, frames=30):
    """ Realiza una transición de zoom entre dos imágenes """
    height, width, _ = img1.shape
    transition = []
    for i in range(frames):
        scale = 1 + (i / frames) * 0.05  # Incremento de zoom
        resized_img2 = cv2.resize(img2, (int(width * scale), int(height * scale)))
        x_offset = (resized_img2.shape[1] - width) // 2
        y_offset = (resized_img2.shape[0] - height) // 2
        zoomed = resized_img2[y_offset:y_offset + height, x_offset:x_offset + width]
        blended = cv2.addWeighted(img1, 1 - i / frames, zoomed, i / frames, 0)
        transition.append(blended)
    return transition

# Función para redimensionar manteniendo la relación de aspecto
def resize_with_aspect_ratio(img, target_height, target_width):
    """ Redimensiona una imagen manteniendo la relación de aspecto original """
    h, w = img.shape[:2]
    aspect_ratio = w / h

    # Si el alto es fijo
    if target_height:
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
        if new_width > target_width:
            new_width = target_width
            new_height = int(new_width / aspect_ratio)
    
    # Si el ancho es fijo
    elif target_width:
        new_width = target_width
        new_height = int(new_width / aspect_ratio)
        if new_height > target_height:
            new_height = target_height
            new_width = int(new_height * aspect_ratio)

    # Redimensionamos la imagen manteniendo la relación de aspecto
    resized_img = cv2.resize(img, (new_width, new_height))

    # Rellenamos con negro si es necesario
    top = (target_height - new_height) // 2
    bottom = target_height - new_height - top
    left = (target_width - new_width) // 2
    right = target_width - new_width - left

    # Crear una nueva imagen de tamaño objetivo y agregar la imagen redimensionada centrada
    final_img = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    final_img[top:top+new_height, left:left+new_width] = resized_img

    return final_img

# Función para generar el video
def create_video_from_images(folder, video_duration, target_height, audio_path=None):
    # Calcular el ancho correspondiente para mantener la relación 16:9
    target_width = int(target_height * 16 / 9)

    # Obtener imágenes de la carpeta
    image_files = sorted([
        os.path.join(folder, f) for f in os.listdir(folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ])
    
    if not image_files:
        print("❌ No se encontraron imágenes en la carpeta.")
        return
    
    print(f"✅ Se han encontrado {len(image_files)} imágenes.")
    
    # Crear un directorio temporal para las imágenes redimensionadas
    temp_dir = tempfile.mkdtemp()
    print(f"🔨 Creando directorio temporal en: {temp_dir}")

    # Redimensionar y guardar imágenes temporales
    images = []
    for i, img_path in enumerate(image_files):
        img = cv2.imread(img_path)
        resized_img = resize_with_aspect_ratio(img, target_height, target_width)  # Redimensionar manteniendo la proporción
        temp_img_path = os.path.join(temp_dir, os.path.basename(img_path))
        cv2.imwrite(temp_img_path, resized_img)  # Guardar temporalmente
        images.append(temp_img_path)
        print(f"🖼️ Redimensionando imagen {i + 1}/{len(image_files)}: {os.path.basename(img_path)}")

    # Duración total por imagen
    num_images = len(images)
    image_duration = video_duration / num_images

    # Configurar el VideoWriter
    first_image = cv2.imread(images[0])
    height, width, _ = first_image.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Códec para mp4
    out = cv2.VideoWriter('video_resultado.mp4', fourcc, 30.0, (width, height))

    print("🎬 Comenzando a generar el video...")

    # Procesar las imágenes con transiciones (solo 'fade' y 'zoom')
    transition_types = ['fade', 'zoom']  # Eliminamos 'slide'
    last_image = None

    for i, img_path in enumerate(images):
        img = cv2.imread(img_path)

        # Si no es la primera imagen, agregar transición con la anterior
        if last_image is not None:
            transition_type = random.choice(transition_types)
            print(f"🔄 Aplicando transición de tipo '{transition_type}' entre imagen {i}/{len(images)} y la siguiente.")
            if transition_type == 'fade':
                transition_frames = fade_transition(last_image, img)
            elif transition_type == 'zoom':
                transition_frames = zoom_transition(last_image, img)

            # Agregar la transición al video
            for frame in transition_frames:
                out.write(frame)

        # Agregar la imagen al video
        print(f"📽️ Añadiendo imagen {i + 1}/{len(images)} al video.")
        for _ in range(int(image_duration * 30)):  # 30 fps
            out.write(img)

        last_image = img  # Guardar la imagen actual como la última

    # Finalizar el video
    out.release()

    # Si se proporcionó un archivo de audio, lo añadimos al video
    if audio_path and os.path.isfile(audio_path):
        print(f"🎶 Añadiendo audio al video desde: {audio_path}")
        # Utilizamos FFmpeg para añadir el audio al video
        subprocess.run([
            'ffmpeg', '-y', '-i', 'video_resultado.mp4', '-i', audio_path,
            '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental',
            '-shortest', 'video_resultado_con_audio.mp4'
        ])
        print("✅ Video con audio generado: video_resultado_con_audio.mp4")
        os.remove('video_resultado.mp4')  # Eliminar video sin audio
    else:
        print("❌ No se proporcionó un archivo de audio válido.")

    # Limpiar archivos temporales
    rmtree(temp_dir)
    print("🗑️ Limpiando archivos temporales...")

# Función principal
def main():
    folder = input("Introduce la ruta de la carpeta con imágenes: ").strip()
    video_duration = float(input("Duración total del video (en segundos): ").strip())
    target_height = int(input("Introduce la resolución de alto para el video (en píxeles): ").strip())
    audio_path = input("Introduce la ruta del archivo de audio (o presiona Enter para omitir): ").strip() or None
    
    if not os.path.isdir(folder):
        print("❌ La ruta proporcionada no es válida.")
        return
    
    create_video_from_images(folder, video_duration, target_height, audio_path)

if __name__ == "__main__":
    main()
