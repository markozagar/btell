from django.shortcuts import render
from django import http


def index(request: http.HttpRequest) -> http.HttpResponse:
    return http.HttpResponse('IT WORKS MAYBE')
