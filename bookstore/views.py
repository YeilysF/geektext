from django.shortcuts import render
from bookstore.models import Book, Author, Genre
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower


def index(request):
    model = Book
    queryset = model.objects.all()
    context = {'my_book_list': queryset }
    return render(request, 'index.html', context=context)


def about(request):
    return render(request, 'about.html', {'title': 'About'})

def browse_sort_view(request):
    model = Book

    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    ordering = Lower(order_by)
    if direction == 'desc':
        ordering = '-{}'.format(ordering)
    p = (order_by==None)
    q = (order_by!=None)
    genre_selection = request.GET.get('genre_selection')
    genre_choice = Book.genre
    genre_filter = (genre_selection!=None)
    #fiction_filter = (genre_selection=='fiction')
    #nonfiction_filter = (genre_selection=='nonfiction')

    #queryset = model.objects.all().order_by(ordering)
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
        'books' : books,
        'order_by' : order_by,
        'direction': direction,
        'p': p,
        'q': q,
        'genre_selection': genre_selection,
        'genre_choice': genre_choice,
        'genre_filter': genre_filter
    }
    return render(request, 'browse_sort.html', context=context)
