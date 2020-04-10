from django import template
from bookstore.models import WishlistBook


register = template.Library()


@register.simple_tag
def get_wishlist_books(wishlist_id):
	print(wishlist_id)
	return WishlistBook.objects.select_related('wb_book').filter(wb_wishlist_id=wishlist_id)