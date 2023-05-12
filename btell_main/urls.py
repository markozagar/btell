from django.urls import path
from btell_main import views

urls = [
    path('', views.index, name='btell_index')
]