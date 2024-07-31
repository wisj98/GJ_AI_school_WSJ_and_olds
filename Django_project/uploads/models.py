from django.db import models
from django.conf import settings

class Upload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    result_image = models.ImageField(upload_to='results/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)