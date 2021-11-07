from datetime import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Post, User, Like
from .forms import SignUpForm, BootstrapPostForm

class PostListView(generic.ListView):
    """Renders all posts page."""
    model = Post
    paginate_by = 5
    #ordering = ['all_likes']
    template_name = 'app/blog.html'


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

class PostDetailView(generic.DetailView):
    """Пока не используется, отображение поста через класс"""
    model = Post
    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['is_liked'] = Like.is_liked(post, self.request.user)
        return context
    template_name = 'app/blog.html'


def post(request, post_id):
    """Renders the post page."""
    assert isinstance(request, HttpRequest)
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'GET':
        is_liked = Like.is_liked(post, request.user)
        return render(
            request,
            'app/blog.html',
            {
                'title': post.title,
                'post': post,
                'is_liked': is_liked,
            }   
        )

    if request.method == 'POST':
        form = BootstrapPostForm(request.POST, instance=post)   # TODO: Надо бы разобраться че к чему тут
        if post.author != request.user:
            raise PermissionDenied
        else:
            print(form.errors.as_json())
            print(form.is_valid())
            print(form.non_field_errors)
            if form.is_valid():
                print(form.non_field_errors())
                post = form.save(commit=False)
                post.last_edited = datetime.now().strftime("%d/%m/%Y")
                post.categories.set(form.cleaned_data['categories'])
                post.save()
                return redirect('/post/' + str(post_id))
            else:
                form = BootstrapPostForm(instance=post)
            return render(
                request,
                'app/post_edit.html',
                {
                    'post': Post.objects.get(id=post_id),
                    'form': form,
                }
            )

@login_required(login_url='/login/')
def like_post(request, post_id):
    """Like or delete like on post."""
    assert isinstance(request, HttpRequest)
    post = get_object_or_404(Post, id=post_id)
    if Like.is_liked(post, request.user):
        Like.remove_like(post, request.user)
    else:
        Like.add_like(post, request.user)
    print(Like.objects.count())    # Для отладки
    return HttpResponse(
            json.dumps({
                "is_liked": Like.is_liked(post, request.user),
                "like_count": post.total_likes,
            }),
            content_type="application/json"
        )


@login_required(login_url='/login/')
def post_delete(request, post_id):
    """Deleting post in user blog"""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            raise PermissionDenied
        else:
            post.delete()
    return redirect('my_blog')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class MyPostListView(generic.ListView):
    """Renders all user posts page."""
    model = Post
    def get_queryset(self):
        """Gets user posts"""
        user = self.request.user
        queryset = Post.objects.filter(author=user)
        return queryset
    paginate_by = 5
    template_name = 'app/blog.html'


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
            'blogger': User.objects.get(id=author_id),
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
            post.categories.set(form.cleaned_data['categories'])    # Добавляем many-to-many категории после сохранения
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
