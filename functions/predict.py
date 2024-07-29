import tensorflow as tf
import pandas as pd
import pickle
from tensorflow.keras.preprocessing import image
import numpy as np

with open('models/label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)
with open('models/width_height.pkl', 'rb') as file:
    image_width, image_height = pickle.load(file)
model = tf.keras.models.load_model('models/my_model.keras')

test = pd.read_csv("data/modi_train.csv")

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

for i in range(len(test)):
    img_path = test.iloc[i]["path"]

    img = image.load_img(img_path, target_size=(image_width, image_height))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)

    top_3_indices = np.argsort(pred[0])[-3:][::-1]
    top_3_probs = pred[0][top_3_indices]
    top_3_classes = label_encoder.inverse_transform(top_3_indices)

    truth = img_path.split('/')[1]
    
    is_correct = top_3_classes[0] == truth
    is_in_top3 = truth in top_3_classes
    
    result["path"].append(img_path)
    result["first"].append(top_3_classes[0])
    result["first_per"].append(top_3_probs[0])
    result["second"].append(top_3_classes[1])
    result["second_per"].append(top_3_probs[1])
    result["third"].append(top_3_classes[2])
    result["third_per"].append(top_3_probs[2])
    result["TF"].append(is_correct)
    result["top3_TF"].append(is_in_top3)
    
    if truth not in total_predictions:
        total_predictions[truth] = 0
        correct_predictions[truth] = 0
        top3_correct_predictions[truth] = 0
    total_predictions[truth] += 1
    
    if is_correct:
        correct_predictions[truth] += 1
    
    if is_in_top3:
        top3_correct_predictions[truth] += 1

result_df = pd.DataFrame(result)

result_df.to_csv("result/results.csv", index=False)

accuracy_per_class = {
    "클래스": [],
    "총 예측 수": [],
    "정확한 예측 수": [],
    "정확도": [],
    "상위 3개 안에 정답 수": [],
    "상위 3개 정답률": []
}

for cls in total_predictions:
    accuracy_per_class["클래스"].append(cls)
    accuracy_per_class["총 예측 수"].append(total_predictions[cls])
    accuracy_per_class["정확한 예측 수"].append(correct_predictions[cls])
    accuracy_per_class["정확도"].append(correct_predictions[cls] / total_predictions[cls])
    accuracy_per_class["상위 3개 안에 정답 수"].append(top3_correct_predictions[cls])
    accuracy_per_class["상위 3개 정답률"].append(top3_correct_predictions[cls] / total_predictions[cls])

accuracy_df = pd.DataFrame(accuracy_per_class)

accuracy_df.to_csv("result/class_accuracy.csv", index=False)

print(result_df.head())
print(accuracy_df.head())
