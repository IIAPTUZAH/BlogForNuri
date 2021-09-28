"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, Category
from .forms import SignUpForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    most_liked_posts = Post.objects.order_by('-likes')[:3]
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'posts':most_liked_posts,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def post(request, post_id):
    """Renders the post page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/post.html',
        {
            'post':Post.objects.get(id=post_id),
        }
    )

def signup(request):
    """Renders the sign up page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(
        request,
       'app/signup.html', 
       {
           'form': form,
       }
    )

def blogger(request, author_id):
    """Renders page about blogger"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogger.html',
        {
            'user':User.objects.get(id=author_id),
            'blog':Post.objects.filter(author=author_id),
            'category':Category.objects.all()
        }
    )
