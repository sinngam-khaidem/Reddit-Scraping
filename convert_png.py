from PIL import Image
import os
import glob

SUBREDDIT_NAME = "RoastMe"
CATEGORY = "top"
# Define the directory containing the images
input_directory = f"media_files/{SUBREDDIT_NAME}/{CATEGORY}"
output_directory = f"png_media_files/{SUBREDDIT_NAME}/{CATEGORY}"

os.makedirs(output_directory, exist_ok=True)

# Define the supported extensions
supported_extensions = ['*.jpeg', '*.jpg', '*.png', '*.webp']

# Iterate over each file in the input directory with supported extensions
for extension in supported_extensions:
    for file_path in glob.glob(os.path.join(input_directory, extension)):
        # Open the image file
        with Image.open(file_path) as img:
            # Get the base name of the file (without extension)
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # Define the output path with PNG extension
            output_path = os.path.join(output_directory, f"{base_name}.png")
            
            # Convert and save the image as PNG
            img.save(output_path, 'PNG')
            
print("Conversion to PNG completed.")
