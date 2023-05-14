from django.contrib.auth import views as auth_views
from django.urls import path

from btell_main.views import index as index_view

from btell_main.forms import login, register


urls = [
    path('', index_view.index, name='btell_index'),
    # Authentication views
    path('a/login.html/', login.LoginPage.as_view(), name='login'),
    path('a/register.html/', register.RegisterPage.as_view(), name='register'),
    path('a/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
