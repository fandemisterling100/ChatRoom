from django.shortcuts import render
from .forms import LoginForm, RegisterForm, ChatroomForm
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
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required
def index(request):
    if request.method == "POST":
        # Redirect the user to the chatroom typed
        room_name = request.POST["room_name"]
        
        return HttpResponseRedirect(reverse("room", kwargs={'room_name': room_name}))
    else:
        # Ask to the user for a chatroom to join
        return render(request, "chatroom/index.html", {
            "form": ChatroomForm()
        })


@login_required
def room(request, room_name):
    """Render the chatroom page for a specific room name
        room_name: str
    """
    
    # Load the last 50 messages from the chosen room
    messages = Message.objects.filter(room_name=room_name)[:50]
    
    return render(request, "chatroom/room.html", {
        "room_name": room_name,
        "messages": messages
    })