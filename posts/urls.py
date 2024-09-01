from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('',views.posts_list, name="list"),
    path('<slug:slug>', views.post_page, name="page"),
    path('new-post/', views.post_new, name="new-post"),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    #path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    #path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('like/', views.like_post, name='like_post'),
]
