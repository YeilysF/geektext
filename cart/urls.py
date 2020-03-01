from django.conf.urls import url

from . import views

urlpatterns = [url(r'^$', views.cart_view, name='cart'),
              url(r'^add/(?P<book_id>\d+)/$', views.add_to_cart, name='add-cart'),
              # url(r'^remove/(?P<book_id>\d+)/$',views.remove_from_cart, name='remove-cart'),

               ]