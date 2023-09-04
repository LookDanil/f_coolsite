from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat_slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form_input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина заголовка слишком большая!')
        return title


class AddUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form_input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form_input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
