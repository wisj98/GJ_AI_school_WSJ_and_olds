import tensorflow as tf
import pandas as pd
import pickle
import os
from tensorflow.keras.preprocessing import image
import numpy as np
import time 

with open('models/label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)
model = tf.keras.models.load_model('models/my_model.keras')

test = pd.read_csv("data/train.csv")
for i in range(len(test)):
    img_path = test.iloc[i]["path"]
    img = image.load_img(img_path, target_size=(198, 177))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    pred = model.predict(img_array)
    predicted_class = np.argmax(pred, axis=1)
    truth = img_path.split('/')[1]
    count = 0
    false = []
    print(label_encoder.inverse_transform(np.argmax(pred, axis=1)))
print(count)
    