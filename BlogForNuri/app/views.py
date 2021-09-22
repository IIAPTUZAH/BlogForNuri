"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import Post


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
