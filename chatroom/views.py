from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
    pass

def logout_view(request):
    pass

@login_required
def index(request):
    return render(request, "chatroom/index.html")

