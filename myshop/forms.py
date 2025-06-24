from django import forms
from .models import Product
from django.contrib.auth.forms import AuthenticationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control'
        })
    )
