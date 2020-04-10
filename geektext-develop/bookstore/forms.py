from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Wishlist, Comment


class NewWishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['wishlist_name']

class UpdateWishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['wishlist_name']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('anonymous', 'body')
