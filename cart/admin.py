from django.contrib import admin
from .models import Cart, SavedItem, Order, OrderItem, CartItem, Coupon

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(SavedItem)
admin.site.register(OrderItem)
admin.site.register(Coupon)

