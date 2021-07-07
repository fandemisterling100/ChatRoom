from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import *

def login_view(request):
    if request.method == "POST":
        
        # Get values from user to authenticate
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check authentication
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chatroom/login.html", {
                "message": "Invalid Credentials",
                "form": LoginForm()
            })
    else:
        return render(request, "chatroom/login.html", {
            "form": LoginForm()
        })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        # Server-side validation for password and confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chatroom/register.html", {
                "message": "Passwords must match",
                "form": RegisterForm(request.POST)
            })
        
        # Create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chatroom/register.html", {
                "message": "This username already exists, please try another one.",
                "form": RegisterForm(request.POST)
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chatroom/register.html", {
            "form": RegisterForm()
        })

def logout_view(request):
    pass

@login_required
def index(request):
    return render(request, "chatroom/index.html")

