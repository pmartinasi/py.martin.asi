import os
import sys
import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def get_dominant_colors(image_path, num_colors=5):
    image = Image.open(image_path)
    image = image.convert("RGB")
    image = image.resize((100, 100))  # Resize to speed up processing
    pixels = np.array(image).reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=42)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    
    return [tuple(color) for color in colors]

def create_palette_image(image_path, colors):
    image = Image.open(image_path)
    width, height = image.size
    palette_width = width // 5  # Adjust width for the palette
    new_width = width + palette_width
    
    # Create new image with additional width
    palette_image = Image.new("RGB", (new_width, height), "white")
    palette_image.paste(image, (0, 0))
    
    # Draw color blocks
    block_height = height // len(colors)
    for i, color in enumerate(colors):
        block = Image.new("RGB", (palette_width, block_height), color)
        palette_image.paste(block, (width, i * block_height))
    
    output_path = os.path.splitext(image_path)[0] + "_palette.jpg"
    palette_image.save(output_path)
    print(f"Palette image saved: {output_path}")

def process_image(image_path):
    colors = get_dominant_colors(image_path)
    create_palette_image(image_path, colors)

def process_directory(directory):
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(valid_extensions)]
    
    if not image_files:
        print("No valid image files found in the directory.")
        return
    
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        process_image(image_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path_or_directory>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    if os.path.isdir(input_path):
        process_directory(input_path)
    elif os.path.isfile(input_path):
        process_image(input_path)
    else:
        print("Invalid path provided.")
