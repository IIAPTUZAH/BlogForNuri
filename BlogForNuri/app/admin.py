from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Случайно добавил пару категорий кликом"""

    list_display = ('id', 'name')