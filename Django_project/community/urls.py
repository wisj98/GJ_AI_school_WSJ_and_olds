from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.board_view, name='board'),
    path('board/search/', views.search_board, name='search_board'),
    path('board/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.comment_add, name='comment_add'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
]