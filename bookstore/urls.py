from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('browse_sort/', views.browse_sort_view, name='browse_sort')
]