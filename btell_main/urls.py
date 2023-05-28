"""Do I really need to explain this?"""
from django import urls
from django.contrib.auth import views as auth_views

from btell_main.views import index as index_view
from btell_main.views import story_list

from btell_main.forms import login, register


urls = [
    urls.path('', index_view.index, name='btell_index'),
    urls.path('stories', story_list.story_list, name='story_list'),
    # Authentication views
    urls.path('a/login.html/', login.LoginPage.as_view(), name='login'),
    urls.path('a/register.html/', register.RegisterPage.as_view(), name='register'),
    urls.path('a/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
