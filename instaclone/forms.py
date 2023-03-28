from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'password1', 'password2', 'name', 'user_info', 'phone_number', 'gender']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_info': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(choices=CustomUser.GENDER_CHOICES, attrs={'class': 'form-control'}),
            }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'description']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

