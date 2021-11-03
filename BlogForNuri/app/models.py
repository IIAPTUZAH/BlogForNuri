"""
Definition of models.
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


class Profile(models.Model):
    """Модель пользователя. У меня был план, но я его забыл."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Like(models.Model):
    """Модель лайка"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #like = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def add_like(obj, user):
        """Лайкает obj"""
        obj_type = ContentType.objects.get_for_model(obj)
        like, is_created = Like.objects.get_or_create(
            content_type=obj_type, object_id=obj.id, user=user)
        return like

    def remove_like(obj, user):
        """Удаляет лайк с obj"""
        obj_type = ContentType.objects.get_for_model(obj)
        Like.objects.filter(
            content_type=obj_type, object_id=obj.id, user=user
        ).delete()

    def is_liked(obj, user) -> bool:
        """Проверяет, лайкнул ли user obj"""
        if not user.is_authenticated:
            return False
        obj_type = ContentType.objects.get_for_model(obj)
        likes = Like.objects.filter(
            content_type=obj_type, object_id=obj.id, user=user)
        return likes.exists()

    def get_likes(obj):
        """Получает всех пользователей, которые лайкнули obj"""
        obj_type = ContentType.objects.get_for_model(obj)
        return User.objects.filter(
            likes__content_type=obj_type, likes__object_id=obj.id)

    def __str__(self):
        return self.like


class Category(models.Model):
    """Модель категорий постов"""
    name = models.CharField(max_length=80, help_text='Выберите категорию')

    def __str__(self):
        return self.name

    class Meta: 
        ordering = ('name',)


class Post(models.Model):
    """Модель постов"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    test_likes = GenericRelation(Like)
    categories = models.ManyToManyField(Category)

    def display_categories(self):
        """Отображаем категорию поста"""
        return ', '.join([ categories.name for categories in self.categories.all() ])
    display_categories.short_description = 'Categories'

    class Meta:
        ordering = ('title',)

    @property
    def total_likes(self):
        """Возвращаем общее количество лайков у поста"""
        return self.test_likes.count()

    def __str__(self):
        """Возвращаем название поста и автора"""
        return '{} автор @{}'.format(self.title, self.author.username)


