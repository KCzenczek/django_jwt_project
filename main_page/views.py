import datetime as dt
import jwt
import time
from cryptography.hazmat.primitives import serialization

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
    payload_data = {
        "username": username,
        "exp": dt.datetime.utcnow() + dt.timedelta(seconds=60),
        "iat": dt.datetime.utcnow()
    }

    # private key
    private_key_file = open('private_key', 'r').read()
    private_key = serialization.load_ssh_private_key(private_key_file.encode(), password=b'')

    # token creation
    new_token = jwt.encode(
        payload=payload_data,
        key=private_key,
        algorithm='RS256'
    )

    # public key and decoding for testing below only
    public_key_file = open('public_key.pub', 'r').read()
    public_key = serialization.load_ssh_public_key(public_key_file.encode())

    token_decoded = jwt.decode(jwt=new_token, key=public_key, algorithms=['RS256', ])
    print("Encoded date: ", token_decoded["exp"], "Decoded date: ", dt.date.fromtimestamp(token_decoded["exp"]))

    # time.sleep(30)
    try:
        token_decoded_after_30_sec = jwt.decode(jwt=new_token, key=public_key, algorithms=['RS256', ])
    except jwt.ExpiredSignatureError:
        token_decoded_after_30_sec = ""
        print("Token has expired!")

    if token_decoded_after_30_sec:
        print("Token is valid!")

    # as alternative: jwt with algorythm HS256 and secret_key only

    # secret_key = "super long, super random and super secret"
    # new_token = jwt.encode(
    #     {
    #         "username": username,
    #         "exp": dt.datetime.utcnow() + dt.timedelta(days=2),
    #         "iat": dt.datetime.utcnow()
    #     },
    #     secret_key,
    #     algorithm='HS256'
    # )

    return render(
        request, 'main_page/token_generation.html', context={
            "token": new_token,
            # "token_decoded": token_decoded
        }
    )
