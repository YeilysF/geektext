from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'bookstore-home'),
    path('about/', views.about, name = 'bookstore-about')
]
