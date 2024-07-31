from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # home view를 루트 URL로 설정
]