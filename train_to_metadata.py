import os
import pandas as pd
from PIL import Image

folder_list = os.listdir("images")
file_list = []
meme_class = []
for i in folder_list:
    file_list += list(map(lambda x: f"images/{i}/{x}",os.listdir(f"images/{i}")))
print(file_list)

for i in range(len(file_list)):
    name = file_list[i].split('.')
    if name[-1] != "jpg":
        img = Image.open(file_list[i]).convert('RGB')
        img.save(name[0] + ".jpg")
        os.remove('.'.join(name))
        file_list[i] = name[0] + ".jpg"

train_data = pd.DataFrame({"Path" : file_list})
print(train_data.head())

sizes = train_data["Path"].apply(lambda x: Image.open(x).size)
train_data["h"] = sizes.apply(lambda x: x[0])
train_data["w"] = sizes.apply(lambda x: x[1])
train_data["Class"] = train_data["Path"].apply(lambda x: int(x.split('/')[1][4:]))

print(train_data)

train_data.to_csv("data/train.csv", index = False)