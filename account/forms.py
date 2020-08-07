from django import forms
from .validators import validate_email


# login form
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=60, label='', widget=forms.TextInput(attrs={'placeholder': 'Enter valid email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Enter valid password'}))


# register form
class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=60, validators=[validate_email], label='', widget=forms.TextInput(attrs={'placeholder': 'Enter valid email'}))
    username = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Enter valid user name'}))
    phone = forms.CharField(max_length=9, label='', widget=forms.TextInput(attrs={'placeholder': 'Enter valid phone'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Enter valid password'}))
