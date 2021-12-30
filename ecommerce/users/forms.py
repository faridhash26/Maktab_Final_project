from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255, min_length=3, label='username')
    password = forms.CharField(widget=forms.PasswordInput)