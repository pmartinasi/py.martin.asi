from PIL import Image
import os, sys, glob

def pixelate(input_file_path, pixel_size=8):
    image = Image.open(input_file_path)
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    
    # Create the new filename by appending "piexeled.png" to the original file name
    # Remove the file extension before appending
    base_name = os.path.splitext(input_file_path)[0]
    new_file_path = f"{base_name}_pixelate.png"
    
    # Save the pixelated image
    image.save(new_file_path)
    print(f"Pixelated image saved as: {new_file_path}")

def list_files(directory, dataType="*.png"):
    # Use glob to find all .png files in the specified directory
    png_files = glob.glob(os.path.join(directory, str(dataType)))
    return png_files

if __name__ == "__main__":
    # Check if the directory path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <directory_path>")
        sys.exit(1)

    # Get the directory path from command-line arguments
    directory_path = sys.argv[1]

    # Check if the provided path is a directory
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)
        
    
    #dir_types = ["*.png", "*.jpg", "*.tif", "*.tiff"]
    
    dir_types = ["*.tif"]
    
    # List all PNG files in the directory
    for i in dir_types:
        files_found = list_files(directory_path, str(i))
        if not files_found:
            print(f"No {i} files found in {directory_path}.")
        else:
            print(f" {i}  files found in {directory_path}:")
            for file in files_found:
                print(file)
                pixelate(file)