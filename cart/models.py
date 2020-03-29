from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from bookstore.models import Book
from users.models import Profile


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created_time = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['created_time']

    def __str__(self):
        return self.cart_id

    #user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    #updated_time = models.DateTimeField(blank=True, null=True)
    #active = models.BooleanField(default=True)
    #payment_type = models.CharField(max_length=100, null=True)
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

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
        return self.book


class OrderItem(models.Model):
    """A model that contains data for an item in an order."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return '%s: %s' % (self.book.book_title, self.quantity)

    def get_total_price(self):
        return self.quantity * self.book.price


class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    #book = models.ForeignKey(Book, on_delete=models.CASCADE)
    #cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_time = models.DateField(blank=True, null=True)
    updated_time = models.DateField(blank=True, null=True)

    subtotal = models.DecimalField(default=1000.0, max_digits=300, decimal_places=2)
    tax_amount = models.DecimalField(default=1000.0, max_digits=300, decimal_places=2)

    # shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    # billing_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

    def get_cart_items(self):
        return self.order_items.all()

    def get_total(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_total_price()
        return total

class SavedItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.book


