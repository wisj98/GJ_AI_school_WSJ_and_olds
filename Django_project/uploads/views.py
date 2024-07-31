import os
import numpy as np
import pickle
import tensorflow as tf
import urllib.parse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .forms import ImageUploadForm
from .models import Upload
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.preprocessing import image

try:
    with open(os.path.join(settings.BASE_DIR, 'models/label_encoder.pkl'), 'rb') as file:
        label_encoder = pickle.load(file)
    with open(os.path.join(settings.BASE_DIR, 'models/width_height.pkl'), 'rb') as file:
        image_width, image_height = pickle.load(file)
    model = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, 'models/my_model.keras'))
except Exception as e:
    print(f"Error loading model or label encoder: {e}")

@csrf_exempt
def upload_view(request):
    if request.method == 'POST':
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = fs.path(filename)
        
        # 예측 함수 호출
        top_3_classes, top_3_probs, top_3_images = predict_image(image_path)

        response_data = {
            'top_3_classes': top_3_classes.tolist(),
            'top_3_probs': top_3_probs.tolist(),
            'top_3_images': [urllib.parse.quote_plus(fs.url(img)) if img else None for img in top_3_images],
        }
        
        return JsonResponse(response_data)
    return render(request, 'uploads/upload.html')

def predict_image(image_path):
    img = image.load_img(image_path, target_size=(image_width, image_height))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)

    top_3_indices = np.argsort(pred[0])[-3:][::-1]
    top_3_probs = pred[0][top_3_indices]
    top_3_classes = label_encoder.inverse_transform(top_3_indices)

    images_folder = 'media/images'  # 저장된 이미지 경로를 올바르게 설정
    top_3_images = []
    for class_name in top_3_classes:
        img_path = os.path.join(images_folder, f'{class_name}.jpg')
        if os.path.exists(img_path):
            relative_path = os.path.relpath(img_path, settings.MEDIA_ROOT)
            top_3_images.append(relative_path.replace('\\','/'))
        else:
            top_3_images.append(None)

    return top_3_classes, top_3_probs, top_3_images
