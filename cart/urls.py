from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'cart'

urlpatterns = [
               path('', views.cart_view, name='cart'),
               url(r'', views.add_to_cart, name='add_to_cart'),
               path('', views.remove_from_cart, name='remove_from_cart'),
               path('', views.order_details, name='order_detail'),
               path('', views.get_order, name='get_order')
               # url(r'^remove/(?P<book_id>\d+)/$',views.remove_from_cart, name='remove-cart'),

               ]
