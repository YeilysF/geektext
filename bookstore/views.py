from django.shortcuts import render
from .models import ContactForm
from django.http import HttpResponse

review = [
    {
        'author': 'Eitan Flor',
        'title': 'Review for Harry Potter',
        'content': 'Book Review Details can be here',
        'date_posted': 'January 1, 2020'
    },
]

def about(request):
    return render(request, 'about.html', {'title': 'About'})

def books(request):
    return render(request, 'books.html', {'title': 'Books'})

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

def index(request):
    return render(request, 'index.html', {'title': 'Home Page'})

def reviews(request):
    context = {
        'reviews': review
    }
    return render(request, 'reviews.html', context)

def wishlist(request):
    return render(request, 'wishlist.html', {'title': 'Wishlist'})
from bookstore.models import Book, Author, Genre
from django.views import generic


def index(request):
    model = Book
    queryset = model.objects.all()
    context = {'my_book_list': queryset }
    return render(request, 'index.html', context=context)


def about(request):
    return render(request, 'about.html', {'title': 'About'})
