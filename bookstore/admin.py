from django.contrib import admin

from .models import Author, Genre, Book, Publisher, ShoppingCart

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(ShoppingCart)