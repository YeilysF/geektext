from django.shortcuts import render

from django.urls import path
from . import views

urlpatterns = [
    path('wishlist/', views.wishlist, name='wishlist'),
]

# Create your views here.
