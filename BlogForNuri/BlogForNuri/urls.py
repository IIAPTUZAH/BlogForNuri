"""
Definition of urls for BlogForNuri.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('admin/', admin.site.urls),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/', views.post_create, name='post_create'),
    path('myblog/', views.MyPostListView.as_view(), name='my_blog'),
    path('blogger/<int:author_id>/', views.blogger, name='blogger'),
    #path('post/<int:id>/', views.PostDetailView.as_view(), name='post'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),  # Работаю над комментами
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('post/<int:post_id>/comment/<int:comment_id>/replay/', views.comment_reply, name='comment_reply'),
    path('bloggers/', views.bloggers, name='bloggers'),
]
