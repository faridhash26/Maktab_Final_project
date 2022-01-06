from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db.models import fields
from django.forms import widgets
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

class UpdateProfileUserForm(forms.ModelForm):
    

    class Meta:
        model=CustomUser
        fields=["username" , "email" , "phone" , "image" , "address" , "zip" ,"city"]
        widgets={
        "username":forms.TextInput(attrs={'class':'w3-input w3-border'}),
        "phone":forms.TextInput(attrs={'class':'w3-input w3-border'}),
        "image": forms.FileInput(attrs={'class':'w3-input w3-border'}),
        "zip":forms.TextInput(attrs={'class':'w3-input w3-border'}),
        "city":forms.TextInput(attrs={'class':'w3-input w3-border'}),
        "address":forms.TextInput(attrs={'class':'w3-input w3-border'}),

    }
    def __init__(self, *args, **kwargs):
        super(UpdateProfileUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class':'w3-input w3-border'})