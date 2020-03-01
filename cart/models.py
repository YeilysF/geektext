from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from bookstore.models import Book
from users.models import Profile


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_time = models.DateField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    payment_type = models.CharField(max_length=100, null=True)
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def add_to_cart(self, book_id):
        book = Book.objects.get(pk=book_id)
        try:
            exist_order = Order.objects.get(book=book, cart=self)
            exist_order.quantity += 1
            exist_order.save()

        except Order.DoesNotExist:
            new_order = Order.objects.create(book=book,cart=self,quantity=1)
            new_order.save()

    def remove_from_cart(self, book_id):
        book = Book.objects.get(pk=book_id)
        try:
            exist_order = Order.objects.get(book=book, cart=self)
            if exist_order.quantity > 1:
                exist_order.quantity -= 1
                exist_order.save()
            else:
                exist_order.delete()
        except Order.DoesNotExist:
            pass


class CartItem(models.Model):
    """A model that contains data for an item in the shopping cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return '%s: %s' % (self.book.book_title, self.quantity)


class OrderItem(models.Model):
    """A model that contains data for an item in an order."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return '%s: %s' % (self.book.book_title, self.quantity)

    def get_total_price(self):
        return self.quantity * self.book.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    # total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_time = models.DateField(blank=True, null=True)
    updated_time = models.DateField(blank=True, null=True)

    subtotal = models.DecimalField(default=1000.0, max_digits=300, decimal_places=2)
    tax_amount = models.DecimalField(default=1000.0, max_digits=300, decimal_places=2)

    # shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    # billing_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_total_price()
        return total

class SavedItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.book.book_title


