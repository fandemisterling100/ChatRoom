"""
    Forms for registration, login and access to chat rooms.
"""

from .utils import room_name_validator
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               max_length=30)

    password = forms.CharField(label='Password',
                               max_length=32,
                               widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username',
                               max_length=30,
                               min_length=3)

    email = forms.EmailField(label='Email')

    password = forms.CharField(label='Password',
                               max_length=32,
                               widget=forms.PasswordInput)

    confirmation = forms.CharField(label='Confirm Password',
                                   max_length=32,
                                   widget=forms.PasswordInput)


class ChatroomForm(forms.Form):
    room_name = forms.CharField(label='Room Name',
                                max_length=50,
                                required=True,
                                min_length=3,
                                validators=[room_name_validator])
