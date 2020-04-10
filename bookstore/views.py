from django.shortcuts import render, get_object_or_404
from users.forms import UpdateUserForm, UpdateProfileForm
from .models import ContactForm, Book, Author, Genre, Comment
from users.models import Profile
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import NewWishlistForm, UpdateWishlistForm
from .models import ContactForm, Book, Author, Genre, Wishlist, WishlistBook
from django.http import HttpResponse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower
from .forms import CommentForm


def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})


def about(request):
    return render(request, 'about.html', {'title': 'About'})


def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})


def authors(request):
    authors = Author.objects.all()
    return render(request, 'authors.html', {'authors': authors})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message = "{0} has sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['message'])
            # We could use our real email here if we want functionality
            send_mail('New Enquiry', message, sender_email, ['testemail@testemail.com'])
            return HttpResponse('Thanks for contacting us!')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def reviews(request):
    comments = Comment.objects.all()
    return render(request, 'reviews.html', {'comments': comments})


def wishlist(request):
    model = Wishlist
    queryset = model.objects.filter(wishlist_user=request.user)
    # return HttpResponse('Saved ALL OK')
    context = {
        'my_wishlists': queryset
    }

    # return HttpResponse(' OK')
    return render(request, 'wishlist.html', context=context)


def wishlist_add(request):
    if request.method == 'POST':
        form = NewWishlistForm(request.POST)
        if form.is_valid():
            wishlist = form.save()
            wishlist.wishlist_user = request.user
            wishlist.save()
            wishlist_name = form.cleaned_data['wishlist_name']
            messages.success(request, f'Wishlist created successfully.')
            return redirect('wishlist')
    else:
        form = NewWishlistForm()
    return render(request, 'wishlist_add.html', {'form': form})


@login_required
def wishlist_edit(request, wishlist_id):
    if request.method == 'POST':
        # return HttpResponse(wishlist_id)
        form = UpdateWishlistForm(request.POST)
        if form.is_valid():
            wishlist = get_object_or_404(Wishlist, id=wishlist_id)
            wishlist_name = form.cleaned_data['wishlist_name']
            wishlist.wishlist_name = wishlist_name
            wishlist.save()
            messages.success(request, f'Wishlist changes saved successfully!')
            return redirect('wishlist')
    else:
        wishlist = get_object_or_404(Wishlist, id=wishlist_id)
        wishlist_form = UpdateWishlistForm(instance=wishlist)

    context = {
        'wishlist': wishlist,
        'wishlist_form': wishlist_form,
    }

    return render(request, 'wishlist_edit.html', context)


@login_required
def wishlist_delete(request, wishlist_id):
    if request.method == 'GET':
        wishlist = get_object_or_404(Wishlist, id=wishlist_id)
        wishlist.delete()
        messages.success(request, f'Wishlist deleted successfully!')
        return redirect('wishlist')


@login_required
def wishlist_book_remove(request, wishlist_book_id):
    if request.method == 'GET':
        wishlist_book = get_object_or_404(WishlistBook, id=wishlist_book_id)
        wishlist_book.delete()
        messages.success(request, f'Book removed from Wishlist successfully!')
        return redirect('wishlist')


@login_required
def wishlist_book_transfer(request, wishlist_book_id):
    if request.method == 'POST':
        book_wishlist_id = request.POST.get('book_wishlist_id')
        book_wishlist_transfer = request.POST.get('book_wishlist_transfer')
        wishlist_book = get_object_or_404(WishlistBook, id=book_wishlist_id)
        wishlist_book.wb_wishlist_id = book_wishlist_transfer
        wishlist_book.save()
        messages.success(request, f'Wishlist transfer successfully!')
        return redirect('wishlist')
    else:
        wishlist_book = get_object_or_404(WishlistBook, id=wishlist_book_id)
    wishlists = Wishlist.objects.filter(wishlist_user=request.user)

    context = {
        'wishlist_book': wishlist_book,
        'wishlists': wishlists,
    }

    return render(request, 'wishlist_book_transfer.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Profile changes saved successfully!')
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile.html', context)


def browse_sort_view(request):
    model = Book

    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    ordering = Lower(order_by)
    if direction == 'desc':
        ordering = '-{}'.format(ordering)
    p = (order_by == None)
    q = (order_by != None)

    genre_selection = request.GET.get('genre_selection')
    genre_choice = Book.genre
    genre_filter = (genre_selection != None)
    queryset2 = Genre.objects.all()

    top_sellers_button = request.GET.get('top_sellers_button')
    top_sellers_filter = ((top_sellers_button == None) or (top_sellers_button == False))


    ratings_filter_selection = request.GET.get('ratings_filter_selection')
    ratings_filter = (ratings_filter_selection != None)
    ratings_filter_selection2 = request.GET.get('ratings_filter_selection2')
    ratings_filter2 = (ratings_filter_selection2 != None)

    queryset3 = model.objects.all()[3:9]

    r = (genre_filter == True) and (p == True)
    s = (ratings_filter == True) and (ratings_filter2 == True) and (p == True)



    if genre_filter == True:
        queryset = model.objects.all().filter(genre__name__contains=genre_selection).order_by(ordering)
    else:
        queryset = model.objects.all().filter().order_by(ordering)

    if direction == 'price':
        queryset = model.objects.all().filter().order_by('-price')
    if direction == 'rating':
        queryset = model.objects.all().filter().order_by('-rating')
    if direction == 'date':
        queryset = model.objects.all().filter().order_by('-release_date')

    if (ratings_filter == True and ratings_filter2 == True):
        queryset = model.objects.all().filter(rating__gte=ratings_filter_selection, rating__lt=ratings_filter_selection2).order_by("rating")

    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    wishlists = Wishlist.objects.all()

    wishlist_selection = request.GET.get('wishlist_selection')
    is_wishlist = (wishlist_selection != None)
    book_id = request.GET.get('book_id')
    is_book = (book_id != None)
    if is_wishlist == True and is_book == True:
        book = get_object_or_404(Book, id=book_id)
        wishlist = get_object_or_404(Wishlist, id=wishlist_selection)
        obj = WishlistBook(wb_book=book, wb_wishlist=wishlist)
        messages.success(request, f'Book added to wishlist successfully!')
        obj.save()
        return redirect('browse_sort')

    context = {
        'my_book_list': queryset,
        'my_genre_list': queryset2,
        'my_book_list2': queryset3,
        'books': books,
        'order_by': order_by,
        'direction': direction,
        'p': p,
        'q': q,
        'r': r,
        's': s,
        'genre_selection': genre_selection,
        'genre_choice': genre_choice,
        'genre_filter': genre_filter,
        'wishlists': wishlists,
        'top_sellers_button': top_sellers_button,
        'top_sellers_filter': top_sellers_filter,
        'ratings_filter_selection': ratings_filter_selection,
        'ratings_filter': ratings_filter,
        'ratings_filter_selection2': ratings_filter_selection2,
        'ratings_filter2': ratings_filter2
    }
    return render(request, 'browse_sort.html', context=context)


def book_detail_view(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    comments_query = Comment.objects.filter(book=pk)

    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        owns_book = False
        if user_profile.books.filter(pk=pk):
            owns_book = True

        # Comment posted
        new_comment = None
        comment_form = CommentForm(data=request.POST)
        if request.method == 'POST':
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.book = book
                new_comment.profile = request.user
                new_comment.save()
        else:
            comment_form = CommentForm()
    else:
        owns_book = False
        new_comment = None
        comment_form = CommentForm(data=request.POST)
        if request.method == 'POST':
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.book = book
                new_comment.save()

    context = {
        'book': book,
        'comments': comments_query,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'owns_book': owns_book
    }
    return render(request, 'bookstore/book_detail.html', context=context)


class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view(request, primary_key):
        try:
            author = Author.objects.get(pk=primary_key)
        except Author.DoesNotExist:
            raise Http404('Author does not exist')

        return render(request, 'bookstore/author_detail.html', context={'author': author})
