from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # 'main' 앱의 URL 패턴을 루트로 설정
    path('users/', include('users.urls')),
    path('community/', include('community.urls')),
    path('uploads/', include('uploads.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)