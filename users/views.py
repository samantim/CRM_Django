from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

def index(request : HttpRequest):
    if request.user.is_authenticated:
        return render(request, "users/index.html")
    return HttpResponseRedirect(reverse("users:login"))

def login_view(request : HttpRequest):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html",{
                "message" : "Invalid credentials!"
            })
    return render(request, "users/login.html")

def logout_view(request : HttpRequest):
    logout(request)
    return render(request, "users/login.html",{
        "message" : "Successfully Logged out."
    })
