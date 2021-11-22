"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Post, Category, Comment

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class SignUpForm(UserCreationForm):
    """Форма регистрации"""
    first_name = forms.CharField(max_length=30,
                                 required=False, 
                                 label='Имя',
                                 help_text='Необязательное поле.')
    last_name = forms.CharField(max_length=30,
                                required=False,
                                label='Фамилия',
                                help_text='Необязательно поле.')
    email = forms.EmailField(max_length=254,
                             help_text='Обязательное поле. Введите действующий email адрес.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class BootstrapPostForm(forms.ModelForm):
    """Форма создания и редактирования поста"""
    title = forms.CharField(max_length=200,
                            widget=forms.TextInput({
                                            'class': 'form-control',
                                            'placeholder':'Введите название поста'}),
                            required=True,
                            label='Заголовок')
    content = forms.CharField(widget=forms.Textarea({
                                            'class': 'form-control',
                                            'placeholder':'Напишите свой пост'}),
                              label='Текст')
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                        widget=forms.SelectMultiple({
                                            'multiple class': 'form-control',
                                            'style': 'width: auto;',}),
                                        required=True,
                                        label='Категория',
                                        help_text='Выберите одну или несколько категорий')

    class Meta:
        model = Post
        fields = ('title', 'content', 'categories',)


class BootstrapCommentForm(forms.ModelForm):
    """Форма комментария"""
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'BootstrapCommentForm',
            'rows': '2',
            'placeholder': 'Написать комментарий...'
            }))

    class Meta:
        model = Comment
        fields = ['comment']
