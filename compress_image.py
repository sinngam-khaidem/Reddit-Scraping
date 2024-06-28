from PIL import Image
import os
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None

def compress_images_in_dir(src_file_dir, dest_file_dir):
    if not os.path.exists(dest_file_dir):
        os.makedirs(dest_file_dir)
    
    # Iterate over all the files in the input directory
    files = list(os.listdir(src_file_dir))
    for i in tqdm(range(len(files))):
        filename = files[i]
        filepath = os.path.join(src_file_dir, filename)

        # Checking if its an image file that can be opened using pillow.
        try:
            with Image.open(filepath) as img:
                filename_without_ext = os.path.splitext(filename)[0]
                output_filepath = os.path.join(dest_file_dir, f"{filename_without_ext}.png")
                img.thumbnail((500,500), Image.LANCZOS)
                # Remove the old file
                os.remove(filepath)
                img.save(output_filepath, format='PNG')
        except IOError:
            print(f"Skipping non-image file: {filepath}")

if __name__ == "__main__":
    SUBREDDIT = "mildlyinfuriating"
    CATEGORY = "new"

    src_file_dir = f"media_files/{SUBREDDIT}/{CATEGORY}"
    dest_file_dir = f"media_files/{SUBREDDIT}/{CATEGORY}"
    compress_images_in_dir(src_file_dir, dest_file_dir)