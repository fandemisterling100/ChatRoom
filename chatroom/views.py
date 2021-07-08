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
        username = request.POST.get("username")
        password = request.POST.get("password")
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
        
        # Server-side validation of the user data for registration
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            confirmation = form.cleaned_data.get("confirmation")

            if password != confirmation:
                return render(request, "chatroom/register.html", {
                    "message": "Password and confirmation must match",
                    "form": RegisterForm(request.POST)
                })
        else:
            # Show validation errors of the register form
            return render(request, "chatroom/register.html", {
                "message": form.errors,
                "form": RegisterForm(request.POST)
            })

        # Create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        # Handle duplicate values for users
        except IntegrityError:
            return render(request, "chatroom/register.html", {
                "message": "This username already exists.",
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
    """Ask user for a chatroom to join and validate the room name
       before redirect the user
    """
    if request.method == "POST":
        # Server-side validation of the room name typed by the user
        form = ChatroomForm(request.POST)

        # Redirect the user to the chatroom typed
        if form.is_valid():
            # Get the room name
            room_name = form.cleaned_data.get("room_name")
            return HttpResponseRedirect(reverse("room", 
                                                kwargs={'room_name': room_name}))
        else:
            return render(request, "chatroom/index.html", {
                "message": form.errors.as_data().get("room_name")[0],
                "form": ChatroomForm()
            })
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
