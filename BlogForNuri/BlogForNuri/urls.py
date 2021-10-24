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
    path('posts/', views.posts, name='posts'),
    path('post/', views.post_create, name='post_create'),
    path('blogger/<int:author_id>/', views.blogger, name='blogger'),
    path('<int:blogger_id>/posts', views.posts, name='posts'),  # В процессе, нет шаблона блога
    path('post/<int:post_id>/', views.post, name='post'),
    path('bloggers/', views.bloggers, name='bloggers'),
]
