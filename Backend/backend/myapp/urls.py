from django.urls import path
from .views import hello_world, index
urlpatterns =[
    path('hello/', hello_world),
    path('', index),
]