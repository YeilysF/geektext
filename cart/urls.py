from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_page, name='cart_page'),
    path('checkout/', views.cart_checkout, name='checkout'),
    path('checkout_home/', views.checkout_home, name='checkout_home'),
    path('add/<int:book_id>/', views.add_to_cart, name='add_cart'),
    path('remove/<int:book_id>/', views.remove_from_cart, name='remove_cart'),
    path('full_remove/<int:book_id>/', views.remove_full_item, name='remove_full_item'),
    path('save/<int:book_id>/', views.save_for_later, name='save_item'),
    path('delete/<int:item_id>/', views.remove_from_saved, name='remove_save'),
    path('move/<int:item_id>/', views.move_to_cart, name='move_save'),
    path('clear/', views.clear, name='clear_save'),



               ]
