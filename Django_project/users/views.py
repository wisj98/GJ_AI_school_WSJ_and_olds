# main/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from main.models import CustomUser, Post, Comment
from community.forms import PostForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'main/home.html')

# 회원가입
def signup_view(request):
    if request.method == 'POST' :
        username = request.POST['username']
        nickname = request.POST['nickname']
        password = request.POST['password']
        password_confirm = request.POST['confirm_password']

        # 유효성 검사
        if password != password_confirm :
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('signup')
        
        if len(username) < 6 :
            messages.error(request, '아이디는 6자 이상이여야 합니다.')
            return redirect('signup')
        
        if len(nickname) < 3 :
            messages.error(request, '닉네임은 3자 이상이여야 합니다.')
            return redirect('signup')
        
        if len(password) < 8 :
            messages.error(request, '비밀번호는 8자 이상이여야 합니다.')
            return redirect('signup')
        
        if CustomUser.objects.filter(username=username).exists() :
            messages.error(request, '이미 존재하는 아이디입니다.')
            return redirect('signup')
        
        if CustomUser.objects.filter(nickname=nickname).exists():
            messages.error(request, '이미 존재하는 닉네임입니다.')
            return redirect('signup')
        
        # 사용자 생성
        user = CustomUser.objects.create_user(username=username, password=password, nickname=nickname)

        login(request, user)
        return redirect('home')
    else :
        return render(request, 'users/signup.html')
    
# 로그인
def login_view(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request, user)
            return redirect('home')
        else :
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
            return redirect('login')
    else :
        return render(request, 'users/login.html')

# 로그아웃
def logout_view(request) :
    logout(request)
    return redirect('home')