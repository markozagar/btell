from django.core import validators
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from btell_main.models import Profile

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


def index(request: HttpRequest):  # -> http.HttpResponse
    if request.method == 'GET':
        context = {}
        return render(request, 'btell_main/index.html', context)
    
    if request.method == 'POST':
        print("=" * 80)
        print()
        do_what = request.POST.get('do what')

        if do_what == 'log in':
            username = request.POST.get('name')
            if username is None:
                redirect('btell_index')
            password = request.POST.get('password')
            if password is None:
                redirect('btell_index')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
            else:
                redirect('btell_index')  # TODO logging failed message
                

        elif do_what == 'register':
            print(request.POST)
            username = request.POST.get('username')  # check for already occupied name is the last one
            if username is None:
                redirect('btell_index')
            password1 = request.POST.get('password1')
            if password1 is None:
                redirect('btell_index')
            password2 = request.POST.get('password2')
            if password2 is None:
                redirect('btell_index')
            if password1 != password2:
                redirect('btell_index')
            # password complexity checks should go here
            email = request.POST.get('email')
            if email is None:
                redirect('btell_index')
            try:
                validators.validate_email(email)
            except forms.ValidationError:
                redirect('btell_index')
            cookies = request.POST.get('cookies')
            if cookies is None or cookies is False:
                redirect('btell_index')
            try:
                is_user = User.objects.filter(username=username).get()
                redirect('btell_index')
            except User.DoesNotExist:
                User.objects.create_user(username=username, password=password1, email=email) # type: ignore # username arleady cannot be None (first check)
                # user_is_now = User.objects.filter(username=username).get()
                # Profile.objects.create(user=he_is) # apparently it gets created automatically in the models, man
                user = authenticate(request, username=username, password=password1)
                login(request, user)

        elif do_what == 'log out':
            logout(request)



        print()
        print("=" * 80)

        context = {}
        return render(request, 'btell_main/index.html', context)
