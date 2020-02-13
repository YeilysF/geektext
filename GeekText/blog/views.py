from django.shortcuts import render
# from django.http import HttpResponse

posts = [
    {
        'author': 'Eitan Flor',
        'title': 'Blog Post 1',
        'content': 'Statistics',
        'date_posted': 'January 1, 2020'
    },
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
