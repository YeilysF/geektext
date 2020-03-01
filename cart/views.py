from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from bookstore.models import Book
from cart.models import OrderItem, Order, Cart, SavedItem
from users.models import Profile


def cart_view(request):
    return render(request, 'cart_view.html')


@login_required
def add_to_cart(request, book_id):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter books by id
    book = Book.objects.filter(id=book_id.get('book_id', ""))
    if book in request.user.profile.books.all():
        messages.info(request, 'You already own this book')
        return redirect(reverse('my-book-list'))
        # create orderItem of the selected product
    order_item = OrderItem.objects.get_or_create(book=book)
    # create order associated with the user
    user_order = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)

    # show confirmation message
    messages.info(request, "item added to cart")
    #return redirect(reverse('books:my-book-list'))

@login_required()
def remove_from_cart(request, book_id):
    item_to_delete = OrderItem.objects.filter(pk=book_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Book has been deleted")


def order_details(request, **kwargs):
    exist_order = get_order(request)
    context = {
        'order': exist_order
    }
    return render(request, 'cart_view.html', context)

def get_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(user=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0