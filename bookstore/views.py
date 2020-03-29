from django.shortcuts import render, get_object_or_404
from .models import ContactForm, Book, Author, Genre, Comment
from users.models import Profile
from django.http import HttpResponse, Http404
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower
from .forms import CommentForm

review = [
    {
        'author': 'Eitan Flor',
        'title': 'Review for Harry Potter',
        'content': 'Book Review Details can be here',
        'date_posted': 'January 1, 2020'
    },
]


def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books' : books})


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
    context = {
        'reviews': review
    }
    return render(request, 'reviews.html', context)


def wishlist(request):
    return render(request, 'wishlist.html', {'title': 'Wishlist'})


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
    # fiction_filter = (genre_selection=='fiction')
    # nonfiction_filter = (genre_selection=='nonfiction')

    # queryset = model.objects.all().order_by(ordering)
    queryset2 = Genre.objects.all()
    if genre_filter == True:
        queryset = model.objects.all().filter(genre__name__contains=genre_selection).order_by(ordering)
    else:
        queryset = model.objects.all().filter().order_by(ordering)

    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 4)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    context = {
        'my_book_list': queryset,
        'my_genre_list': queryset2,
        'books': books,
        'order_by': order_by,
        'direction': direction,
        'p': p,
        'q': q,
        'genre_selection': genre_selection,
        'genre_choice': genre_choice,
        'genre_filter': genre_filter
    }
    return render(request, 'browse_sort.html', context=context)


def book_detail_view(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    comments_query = Comment.objects.filter(book=pk)

    user_profile = Profile.objects.get(user=request.user)
    owns_book = False
    if user_profile.books.filter(pk=pk):
        owns_book = True

    # Comment posted
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.profile = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

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
