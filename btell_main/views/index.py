from django.core import validators
from django import forms, http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from btell_main.views import context as btell_context


def index(request: http.HttpRequest) -> http.HttpResponse:
    ctx = {}
    btell_context.context_add_user_info(request, ctx)
    return render(request, 'btell_main/index.html', ctx)
