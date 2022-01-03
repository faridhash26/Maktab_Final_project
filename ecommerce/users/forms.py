from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms.models import ModelForm

from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255, min_length=3, label='username')
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(max_length=20 ,widget=forms.PasswordInput(attrs={}) )
    class Meta:
        model = CustomUser
        fields=["phone","email","username" , "password","password2"]
