from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from bookstore.models import Book
from cart.models import OrderItem, Order
from users.models import Profile


def cart_view(request, ):
    return render(request, 'cart_view.html')

def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    book = Book.objects.filter(id=kwargs.get('book_id', "")).first()
    # check if the user already owns this product
    if book in request.user.profile.books.all():
        messages.info(request, 'You already own this book')
        return redirect(reverse('bookstore:browse_sort'))
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(book=book)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('bookstore:browse_sort'))


