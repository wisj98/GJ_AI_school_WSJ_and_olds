import os
import pandas as pd
from PIL import Image

def metadata_maker():
    csvs = list(map(lambda x: f"images_csv/{x}",os.listdir("images_csv")))
    print(csvs)

    df_list = []
    for i in csvs:
        csv = pd.read_csv(i)
        csv["file"] = csv["file"].apply(lambda x: f"{i}/{x}")
        csv = csv.drop(['ssi','hash','cor','chi','inter'], axis = 1)
        df_list.append(csv)

    df = pd.concat(df_list, ignore_index=True)
    print(df["TF"].value_counts())
    df = df[df["TF"] == 1]
    df = df[df['file'].str.endswith(('jpg', 'png'))]

    print(df["TF"].value_counts())

    new_df = pd.DataFrame()
    new_df["path"] = df["file"].apply(lambda x: "images/" + x.split('/')[1][:-4] + "/" + x.split('/')[-1].split('.')[0] + f".{x.split('/')[-1].split('.')[1]}")
    new_df["size"] = new_df["path"].apply(lambda x: Image.open(x).size)
    new_df["width"] = new_df["size"].apply(lambda x: x[0])
    new_df["height"] = new_df["size"].apply(lambda x: x[1])
    new_df["w/h"] = round(new_df["width"] / new_df["height"], 2)
    new_df["bha"] = round(df["bha"], 2)
    new_df["class"] = new_df["path"].apply(lambda x: x.split("/")[1])
    new_df = new_df.drop("size", axis = 1)
    

    new_df.to_csv(f"data/train.csv", index= False)

if __name__ == "__main__":
    metadata_maker()


