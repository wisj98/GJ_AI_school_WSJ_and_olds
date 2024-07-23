import os
from PIL import Image

folders = os.listdir("images")

for folder in folders:
    dir = f"images/{folder}"
    images = os.listdir(dir)
    for image in images:
        try:
            with Image.open(f"{dir}/{image}") as img:
                img = img.convert('RGB')
                base_name = image.split('.')[0]
                os.remove(f"{dir}/{image}")
                print(f"{dir}/{image}")
                img.save(f"{dir}/{base_name}.gif","gif")
        except:
            continue