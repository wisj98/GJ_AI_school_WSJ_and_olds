import tensorflow as tf
import pandas as pd
import pickle
from tensorflow.keras.preprocessing import image
import numpy as np

def babo(path):
    with open('models/label_encoder.pkl', 'rb') as file:
        label_encoder = pickle.load(file)
    with open('models/width_height.pkl', 'rb') as file:
        image_width, image_height = pickle.load(file)
    model = tf.keras.models.load_model('models/my_model.keras')

    result = {
        "path": [],
        "first": [],
        "first_per": [],
        "second": [],
        "second_per": [],
        "third": [],
        "third_per": [],
        "TF": [],
        "top3_TF": []
    }

    correct_predictions = {}
    total_predictions = {}
    top3_correct_predictions = {}


    img_path = path

    img = image.load_img(img_path, target_size=(image_width, image_height))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)

    top_3_indices = np.argsort(pred[0])[-3:][::-1]
    top_3_probs = pred[0][top_3_indices]
    top_3_classes = label_encoder.inverse_transform(top_3_indices)
    
    return top_3_probs, top_3_classes
