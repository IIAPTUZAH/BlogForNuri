from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .models import Post, User
from .forms import SignUpForm, BootstrapPostForm


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    most_liked_posts = Post.objects.order_by('-likes')[:3]
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
            'posts': most_liked_posts,
        }
    )


def post(request, post_id):
    """Renders the post page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/post.html',
        {
            'title': Post.objects.get(id=post_id).title,
            'post': Post.objects.get(id=post_id),
        }
    )


def posts(request):
    """List of all posts"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Все записи',
            'posts': Post.objects.order_by('-likes'),
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
            'title': 'Регистрация',
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
            'title': User.objects.get(id=author_id).username,
            'user': User.objects.get(id=author_id),
            'blog': Post.objects.filter(author=author_id),
        }
    )


def bloggers(request):
    """Renders list of all bloggers"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/bloggers.html',
        {
            'title': 'Список всех блоггеров',
            'bloggers': User.objects.all(),
        }
    )


@login_required(login_url='/login/')
def post_create(request):
    """Create new post if user is authenticated"""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = BootstrapPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published = datetime.now().strftime("%d/%m/%Y")
            post.save()
            post_id=post.id
            return redirect('/post/' + str(post_id))
    else:
        form = BootstrapPostForm()
    return render(
        request,
        'app/post_edit.html',
        {
            'title': 'Создание поста',
            'form': form,
        }
    )
