import sys
import os
from rembg import remove
from PIL import Image

if len(sys.argv) < 2:
    print("Usage: python app.py <image_path>")
    sys.exit(1)

input_path = sys.argv[1]

if not os.path.exists(input_path):
    print("Error: File does not exist.")
    sys.exit(1)

filename, _ = os.path.splitext(input_path)
output_path = f"{filename}_no_bg.png"

with Image.open(input_path) as img:
    result = remove(img)
    result.save(output_path)

print(f"Background removed successfully: {output_path}")