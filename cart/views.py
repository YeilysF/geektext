from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from bookstore.models import Book
from cart.models import OrderItem, Order, Cart, SavedItem, CartItem
from users.models import Profile


@login_required
def cart_start(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required
def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    try:
        cart = Cart.objects.get(cart_id=cart_start(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_start(request))
    cart.save(),
    try:
        cart_item = CartItem.objects.get(book=book, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(book=book, quantity=1, cart=cart)
        cart_item.save()
    return redirect('cart:cart_page')

def remove_from_cart(request, book_id):
    cart =  Cart.objects.get(cart_id=cart_start(request))
    book = get_object_or_404(Book, id=book_id)
    cart_item = CartItem.objects.get(book=book,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_page')

# cart details
def cart_page(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=cart_start(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.book.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    return render(request, 'cart.html', dict(total=total, counter=counter, cart_items=cart_items))
