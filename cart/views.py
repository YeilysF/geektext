from datetime import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect

from bookstore.models import Book
from cart.forms import CouponApplyForm
from cart.models import OrderItem, Order, Cart, SavedItem, CartItem, Coupon
from bookstore.models import Wishlist, WishlistBook
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
    cart.save()
    try:
        cart_item = CartItem.objects.get(book=book, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(book=book, quantity=1, cart=cart)
        cart_item.save()
    return redirect('cart:cart_page')


@login_required
def add_wishlist_to_cart(request, wishlist_id):
    wishlist_books = WishlistBook.objects.select_related('wb_book').filter(wb_wishlist_id=wishlist_id)
    for wishlist_book in wishlist_books:
        book = Book.objects.get(id=wishlist_book.wb_book_id)
        add_to_cart(request, book.id)
    return redirect('cart:cart_page')


@login_required
def remove_from_cart(request, book_id):
    cart = Cart.objects.get(cart_id=cart_start(request))
    book = get_object_or_404(Book, id=book_id)
    cart_item = CartItem.objects.get(book=book, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_page')


@login_required
def remove_full_item(request, book_id):
    book = Book.objects.get(id=book_id)
    cart = Cart.objects.get(cart_id=cart_start(request))
    cart_item = CartItem.objects.get(book=book, cart=cart)
    cart_item.delete()
    messages.success(request, 'Item has been removed from cart.')

    return redirect('cart:cart_page')


@login_required
def clear_cart(request):
    cart_item = CartItem.objects.all()
    for item in cart_item:
        item.delete()
    return redirect('cart:cart_page')


@login_required
def save_for_later(request, book_id):
    book = Book.objects.get(id=book_id)
    save_book = SavedItem()
    save_book.book = book
    if not SavedItem.objects.filter(book=book).exists():
        save_book.save()
        messages.info(request, "Item has been moved to Save for Later.")
    else:
        messages.info(request, "Item is already in Save for Later.")

    remove_full_item(request, book_id)

    return redirect('cart:cart_page')


@login_required
def remove_from_saved(request, item_id):
    saved_book = SavedItem.objects.get(id=item_id)
    saved_book.delete()

    return redirect('cart:cart_page')


@login_required
def move_to_cart(request, item_id):
    saved_book = SavedItem.objects.get(id=item_id)
    book = saved_book.book

    add_to_cart(request, book.id)
    saved_book.delete()

    return redirect('cart:cart_page')


@login_required
def clear(request):
    saved_books = SavedItem.objects.all()
    for items in saved_books:
        items.delete()
    return redirect('cart:cart_page')

def count(request):
    item_count = 0
    cart = Cart.objects.filter(cart_id=cart_start(request))
    cart_items = CartItem.objects.all().filter(cart=cart[:1])
    for cart_item in cart_items:
        item_count += cart_item.quantity
    return item_count

def checkout_home(request, order_id):
    order_placed = None
    if order_id:
        order_placed = Order.objects.get(id=order_id)
    return render(request, "checkout.html", {'order_placed': order_placed})

def checkout_info(request):
    cart = Cart.objects.get(cart_id=cart_start(request))
    cart_items = CartItem.objects.all().filter(cart=cart)

    order_info = Order.objects.create()
    order_info.save()
    for order_item in cart_items:
        items = OrderItem.objects.create(book=order_item.book, quantity=order_item.quantity,price=order_item.book.price, order=order_info)
        items.save()
        order_item.delete()
        print("The order has been created")
    return redirect("cart:checkout_home", order_info.id)

# cart details
@login_required
def cart_page(request, discount=0, total_before_discount=0, tax_rate=0, subtotal=0, total=0, item_count=0, saved_count=0, coupons=None, cart_items=None, saved_books=None):
    coupon_input = CouponApplyForm()
    try:
        cart = Cart.objects.get(cart_id=cart_start(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        saved_books = SavedItem.objects.all()
        coupons = Coupon.objects.all()
        for cart_item in cart_items:
            item_count = count(request)
            subtotal += float(CartItem.sub_total(cart_item))
            tax_rate = (0.06 * subtotal)
            total = float(subtotal + tax_rate)
            total_before_discount = total
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code=code)
                discount = float(coupon.discount_value)
                if total >= discount:
                    total -= discount
                    messages.info(request, 'Coupon has been applied')
                else:
                    messages.info(request, 'Total cannot be less than discount amount')
            except Coupon.DoesNotExist:
                messages.info(request, 'Coupon is not valid')
        if saved_books:
            saved_count = saved_books.count()
    except ObjectDoesNotExist:
        pass

    return render(request, 'cart.html',
                  dict(coupon_input=coupon_input, discount=discount, total_before_discount=total_before_discount, tax_rate=tax_rate, subtotal=subtotal, total=total, item_count=item_count, saved_count=saved_count, coupons=coupons, cart_items=cart_items, saved_books=saved_books))


