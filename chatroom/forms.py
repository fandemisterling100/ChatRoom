""" Forms needed to LogIn and Register
"""
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)
        
        
class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.CharField(label='Email', max_length=255)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)
    confirmation = forms.CharField(label='Confirm Password', max_length=32, widget=forms.PasswordInput)