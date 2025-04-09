import os
import sys
import cv2
import numpy as np
from tqdm import tqdm

def load_frames(input_dir):
    files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
    return [cv2.imread(os.path.join(input_dir, f)) for f in files]

def save_frame(output_dir, frame, idx):
    filename = os.path.join(output_dir, f"frame_{idx:05d}.png")
    cv2.imwrite(filename, frame)

def interpolate_frames(frames, original_fps, target_fps):
    if target_fps <= original_fps:
        print("El framerate de destino debe ser mayor al original.")
        sys.exit(1)

    factor = target_fps / original_fps
    interpolated_frames = []
    idx = 0

    for i in tqdm(range(len(frames) - 1), desc="Interpolando"):
        interpolated_frames.append(frames[i])  # Original frame

        num_intermediate = int(factor) - 1
        for j in range(1, num_intermediate + 1):
            alpha = j / (num_intermediate + 1)
            interp = cv2.addWeighted(frames[i], 1 - alpha, frames[i + 1], alpha, 0)
            interpolated_frames.append(interp)

    interpolated_frames.append(frames[-1])  # Último frame
    return interpolated_frames

def main(input_dir, output_dir, original_fps, target_fps):
    os.makedirs(output_dir, exist_ok=True)

    print("Cargando frames...")
    frames = load_frames(input_dir)

    print("Interpolando frames...")
    new_frames = interpolate_frames(frames, original_fps, target_fps)

    print("Guardando nuevos frames...")
    for i, f in enumerate(tqdm(new_frames, desc="Guardando")):
        save_frame(output_dir, f, i)

    print(f"Proceso completo. {len(new_frames)} frames generados en '{output_dir}'.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Interpolador de frames (por blending)")
    parser.add_argument("--input", required=True, help="Directorio de entrada con los frames originales")
    parser.add_argument("--output", required=True, help="Directorio de salida para los nuevos frames")
    parser.add_argument("--original_fps", type=int, required=True, help="Framerate original del video")
    parser.add_argument("--target_fps", type=int, required=True, help="Framerate deseado (mayor que el original)")
    args = parser.parse_args()

    main(args.input, args.output, args.original_fps, args.target_fps)
