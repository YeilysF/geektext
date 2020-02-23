from django.db import models
from django.urls import reverse
from django import forms


class Genre(models.Model):
    # Book Genres ; not currently hardcoded but can added via admin app
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=250)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    class Meta:
        ordering = ['last_name', 'first_name']


# Book Model - still some data items to be tweaked and others to be added such as comments, etc.
class Book(models.Model):
    book_title = models.CharField(max_length=200)
    book_cover = models.FileField(null=True, blank=True)
    author = models.ForeignKey('Author', default = 1, on_delete = models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')

    genre = models.ForeignKey('Genre', default = 1, on_delete = models.CASCADE)
    publisher = models.ForeignKey('Publisher', default = 1, on_delete = models.CASCADE)
    release_date = models.DateField(null=True)
    rating = models.DecimalField(decimal_places=2, max_digits=3, default=0)

    def __str__(self):
        return self.book_title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    class Meta:
        ordering = ['book_title']

class ShoppingCart (models.Model):
    quantity = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    time_stamp = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    # include payment type
    payment_type = models.CharField(max_length=100, null=True)


# Contact/Form Model
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
