import os
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.metrics import structural_similarity as ssim
import imagehash
from PIL import Image

def images_to_jpg():
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
                    img.save(f"{dir}/{base_name}.jpg")
                    
            except:
                continue

def resize(origin, new):
    dimensions = (origin.shape[1], origin.shape[0])
    new = cv2.resize(new, dimensions, interpolation=cv2.INTER_AREA)
    return new

def for_ml():
    folders = os.listdir("images")
    print(folders)

    for folder in folders:
        dir = f"images/{folder}"
        images = os.listdir(dir)
        images.sort(key = lambda x: int(x.split(".")[0]))

        origin_1 = cv2.imread(f"{dir}/0.jpg", cv2.IMREAD_GRAYSCALE)
        origin_2 = Image.open(f"{dir}/0.jpg")
        origin_3 = cv2.imread(f"{dir}/0.jpg")
        origin_3 = cv2.cvtColor(origin_3, cv2.COLOR_BGR2HSV)
        origin_3 = cv2.calcHist([origin_3], [0, 1], None, [50, 60], [0, 180, 0, 256])
        cv2.normalize(origin_3, origin_3, 0, 1, cv2.NORM_MINMAX)
        print(origin_1)

        images = images
        ssi = []
        hash = []
        cor = []
        chi = []
        inter = []
        bha = []

        for i in images:
            try:
                img = resize(origin_1, cv2.imread(f"{dir}/{i}", cv2.IMREAD_GRAYSCALE))
                ssi.append(ssim(origin_1, img, Full=True))

                img = Image.open(f"{dir}/{i}")
                hash.append(imagehash.phash(origin_2) - imagehash.phash(img))
                
                img = resize(origin_1, cv2.imread(f"{dir}/{i}")) 
                img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                img = cv2.calcHist([img], [0, 1], None, [50, 60], [0, 180, 0, 256])
                cv2.normalize(img, img, 0, 1, cv2.NORM_MINMAX)

                cor.append(cv2.compareHist(origin_3, img, cv2.HISTCMP_CORREL))
                chi.append(cv2.compareHist(origin_3, img, cv2.HISTCMP_CHISQR))
                inter.append(cv2.compareHist(origin_3, img, cv2.HISTCMP_INTERSECT))
                bha.append(cv2.compareHist(origin_3, img, cv2.HISTCMP_BHATTACHARYYA))

            except:
                for i in [ssi, hash, cor, chi, inter, bha]:
                    i.append(None)

        datas = {
            'file':images,
            'ssi':ssi,
            'hash':hash,
            'cor':cor,
            'chi':chi,
            'inter':inter,
            'bha':bha
        }

        df = pd.DataFrame(datas)
    
    if os.path.isfile(f"images_csv\\{folder}.csv") == False:
        df.to_csv(f"images_csv\\{folder}.csv", index = False)

if __name__ == "__main__":
    images_to_jpg()
    for_ml()