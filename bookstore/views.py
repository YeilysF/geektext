from django.shortcuts import render
from bookstore.models import Book, Author, Genre
from django.views import generic


def index(request):
    model = Book
    queryset = model.objects.all()
    context = {'my_book_list': queryset }
    return render(request, 'index.html', context=context)


def about(request):
    return render(request, 'about.html', {'title': 'About'})
