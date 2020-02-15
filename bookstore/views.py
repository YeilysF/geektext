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

def index(request):
    context = {
        'posts': posts
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html', {'title': 'About'})

def wishlist(request):
    return render(request, 'wishlist.html', {'title': 'Wishlist'})
