from django.shortcuts import render
# from django.http import HttpResponse

posts = [
    {
        'author': 'Eitan Flor',
        'title': 'Review for Harry Potter',
        'content': 'Book Review Details can be here',
        'date_posted': 'January 1, 2020'
    },
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'bookstore/home.html', context)

def about(request):
    return render(request, 'bookstore/about.html', {'title': 'About'})

def wishlist(request):
    return render(request, 'bookstore/wishlist.html', {'title': 'Wishlist'})
