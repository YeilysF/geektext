from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_page, name='cart_page'),
    path('add/<int:book_id>/', views.add_to_cart, name='add_cart'),
    path('add_wishilist/<int:wishlist_id>/', views.add_wishlist_to_cart, name='add_wishilist_cart'),
    path('remove/<int:book_id>/', views.remove_from_cart, name='remove_cart'),


               ]
