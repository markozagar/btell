from django.contrib.auth import views as auth_views
from django.urls import path

from btell_main.views import index as index_view

urls = [
    path('', index_view.index, name='btell_index'),
    # Authentication views
    path('a/login/', auth_views.LoginView.as_view(template_name='btell_main/accounts/login.html', next_page='/'), name='login'),
    path('a/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]