from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_page, name='cart_page'),
    path('checkout_home/<int:order_id>/', views.checkout_home, name='checkout_home'),
    path('checkout_home/', views.checkout_info, name='checkout_info'),
    path('add/<int:book_id>/', views.add_to_cart, name='add_cart'),
    path('add_wishilist/<int:wishlist_id>/', views.add_wishlist_to_cart, name='add_wishilist_cart'),
    path('remove/<int:book_id>/', views.remove_from_cart, name='remove_cart'),
    path('full_remove/<int:book_id>/', views.remove_full_item, name='remove_full_item'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('save/<int:book_id>/', views.save_for_later, name='save_item'),
    path('delete/<int:item_id>/', views.remove_from_saved, name='remove_save'),
    path('move/<int:item_id>/', views.move_to_cart, name='move_save'),
    path('clear/', views.clear, name='clear_save'),
    path('count/', views.count, name='cart_count'),



               ]
