import environ
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from functools import wraps

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()
version = env("VERSION")


def allow_lazy_auth(func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            password = User.objects.make_random_password()
            user_id = get_random_string(length=10)
            user = User.objects.create_user(f"Anon-{user_id}", password=password)
            user.save()
            login(request, user)
        return func(request, *args, **kwargs)
    return wraps(func)(wrapped)


@allow_lazy_auth
def index(request):
    return render(request, "voca_web/index.html", {"version": version})


def about(request):
    return render(request, "voca_web/about.html", {"version": version})


def languages(request):
    return render(request, "voca_web/languages.html", {"version": version})


def contact(request):
    return render(request, "voca_web/contact.html", {"version": version})


def tos(request):
    return render(request, "voca_web/tos.html", {"version": version})


def privacy(request):
    return render(request, "voca_web/privacy.html", {"version": version})
