"""
Definition of models.
"""

from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User 

# Create your models here.

class Profile(models.Model):
    """Модель пользователя. У меня был план, но я его забыл."""
    user = models.OneToOneField(User)

class Post(models.Model):
    """"Модель постов"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_lenght=200)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        """Возвращаем название поста и автора"""
        return '{} by @{}'.format(self.title, self.author.username)

class Category(models.Model):
    """Модель категорий постов"""
    name = models.CharField(max_lenght=80, help_text='Выберите категорию')

    def __str__(self):
        return self.name

    class Meta: 
        ordering = ('name',)

class Like(models.Model):
    """Модель лайка"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.like
