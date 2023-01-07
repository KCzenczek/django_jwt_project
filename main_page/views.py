from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


def main_page(request):
    return render(request, "main_page/main_page.html")


def f_login(request):
    form = AuthenticationForm(request.POST)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = User.objects.get(username=username)
        #TODO check pwd

        if user:
            login(request, user)
            return redirect("/dc")
    context = {
        "form": form,
    }
    return render(request, "django_jwt/login.html", context)


def f_logout(request):
    logout(request)
    return redirect("/dc")
