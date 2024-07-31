from django.shortcuts import render, get_object_or_404, redirect
from main.models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# 게시판 메인
# @login_required
def board_view(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'community/board.html', {'page_obj' : page_obj})

# 새글
# @login_required
def create_post(request):
    if request.method == 'POST' :
        title = request.POST['title']
        content = request.POST['content']
        author = request.user

        Post.objects.create(title=title, content=content, author=author)
        messages.success(request, '글이 성공적으로 작성되었습니다.')
        return redirect('board')
    else :
        return render(request, 'community/create_post.html')

# 내용
# @login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST' :
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else :
        comment_form = CommentForm()
    return render(request, 'community/post_detail.html', {'post':post, 'comment_form':comment_form})

# 수정
# @login_required
def post_edit(request, post_id) :
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author :
        return HttpResponseForbidden("해당 권한이 없습니다.")
    if request.method == 'POST' :
        form = PostForm(request.POST, instance=post)
        if form.is_valid() :
            form.save()
            return redirect('post_detail', post_id=post.id)
    else :
        form = PostForm(instance=post)
    return render(request, 'community/post_edit.html', {'form':form, 'post':post})

# 삭제
# @login_required
def post_delete(request, post_id) :
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author :
        return HttpResponseForbidden("해당 권한이 없는 아이디입니다.")
    if request.method == 'POST' :
        post.delete()
        return redirect('board')
    return render(request, 'community/post_confirm_delete.html', {'post':post})

# 검색
# @login_required
def search_board(request) :
    query = request.GET.get('query', '')
    posts_list = Post.objects.filter(title__icontains=query)
    paginator = Paginator(posts_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'community/board.html', {'page_obj':page_obj})

# 댓글
# @login_required
def comment_add(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST' :
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
        else : 
            print(form.errors)
    return redirect('post_detail', post_id=post.id)