from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import CustomUser, Post, Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'nickname')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'nickname')

# CustomUserAdmin 클래스 정의
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # UserAdmin의 필드셋에 nickname 필드를 추가
    list_display = ['username', 'nickname', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'bio', 'birth_date', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname', 'bio', 'birth_date', 'profile_picture')}),
    )

# CustomUser 모델을 CustomUserAdmin과 함께 관리자 페이지에 등록
try :
    admin.site.register(CustomUser, CustomUserAdmin)
except admin.sites.AlreadyRegistered :
    pass

# Post와 Comment 모델을 관리자 페이지에 등록
try :
    admin.site.register(Post)
except admin.sites.AlreadyRegistered :
    pass

try :
    admin.site.register(Comment)
except admin.sites.AlreadyRegistered :
    pass