import zipfile
import os
import subprocess

# Paths for input and output zip files
input_zip_path = ''
output_zip_path = ''

# Create a directory to extract the files
extract_dir = 'extracted_images'
os.makedirs(extract_dir, exist_ok=True)

# Extract the zip file
with zipfile.ZipFile(input_zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Create a new zip file to store the converted images
with zipfile.ZipFile(output_zip_path, 'w') as output_zip:
    # Iterate over the extracted files
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.lower().endswith('.heic'):
                heic_path = os.path.join(root, file)
                png_filename = os.path.splitext(file)[0] + '.png'
                png_path = os.path.join(root, png_filename)

                # Use ImageMagick to convert HEIC to PNG
                subprocess.run(['convert', heic_path, png_path])

                # Add the converted PNG file to the new zip
                output_zip.write(png_path, os.path.relpath(png_path, extract_dir))

                # Clean up the PNG file after adding it to the zip
                os.remove(png_path)

# Clean up the extracted files
for root, dirs, files in os.walk(extract_dir):
    for file in files:
        os.remove(os.path.join(root, file))
    for dir in dirs:
        os.rmdir(os.path.join(root, dir))
os.rmdir(extract_dir)