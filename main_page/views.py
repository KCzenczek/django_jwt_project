import jwt
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from main_page.forms import LoginForm


def main_page(request):
    return render(request, "main_page/main_page.html")


def f_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                # TODO log as problem with username
                messages.warning(request, 'Ups! sth is wrong with the given username or password')
                return redirect('f_login')

            if password != user.password:
                # TODO log as problem with pwd
                messages.warning(request, 'Ups! sth is wrong with the given username or password')
                return redirect('f_login')

            if user.is_active:
                login(request, user)
                return redirect("/dc")
            else:
                messages.error(request, 'Ups! sth is wrong with user')
                return redirect('f_login')

    return render(request, 'django_jwt/login.html', context={'form': form})


def f_logout(request):
    logout(request)
    return redirect("/dc")


@login_required
def token_generation(request):
    username = request.user.username

    token_jwt = jwt.encode(
        {
            "username": username,
            "exp": datetime.utcnow() + timedelta(seconds=30),
            "iat": datetime.utcnow()
        }, "access_secret", algorithm='HS256'
    )
    return render(request, 'main_page/token_generation.html', context={"token": token_jwt})
