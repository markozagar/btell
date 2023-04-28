from django.shortcuts import render
from django import http, shortcuts


def index(request: http.HttpRequest) -> http.HttpResponse:
    context = {}
    return shortcuts.render(request, 'btell_main/index.html', context)
