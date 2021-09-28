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
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
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
    path('blogger/<int:author_id>/', views.blogger, name='blogger'),
    #path('<int:blogger_id>/posts', views.posts, name='posts'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('bloggers/', views.bloggers, name='bloggers'),
]
