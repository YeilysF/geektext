from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('browse_sort/', views.browse_sort_view, name='browse_sort'),
    path('contact/', views.contact, name='contact'),
    path('reviews/', views.reviews, name='reviews'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('<int:pk>', views.book_detail_view, name='book-detail'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('books/', views.books, name='books'),
    path('authors/', views.authors, name='authors'),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
    path('wishlist_add/', views.wishlist_add, name='wishlist_add'),
    path('wishlist_edit/<int:wishlist_id>', views.wishlist_edit, name='wishlist_edit'),
    path('wishlist_delete/<int:wishlist_id>', views.wishlist_delete, name='wishlist_delete'),
    path('wishlist_book_remove/<int:wishlist_book_id>', views.wishlist_book_remove, name='wishlist_book_remove'),
    path('wishlist_book_transfer/<int:wishlist_book_id>', views.wishlist_book_transfer, name='wishlist_book_transfer'),
]
