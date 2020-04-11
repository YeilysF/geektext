from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from bookstore.models import Book
from users.models import Profile


class Cart(models.Model):
    cart_id = models.CharField(max_length=25, blank=True)
    created_time = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['created_time']

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    """A model that contains data for an item in the shopping cart."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.book.price * self.quantity

    def __str__(self):
        return self.book.book_title


class Order(models.Model):
    created_time = models.DateField(auto_now_add=True, null=True)

    def _str_(self):
        return str(self.id)


class OrderItem(models.Model):
    """A model that contains data for an item in an order."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.book.book_title, self.quantity)


class SavedItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.book_title


class Coupon(models.Model):
    code = models.CharField(default=1, max_length=15, unique=True, null=False)
    discount_value = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return self.code
