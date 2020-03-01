from django import forms
#Allow users to change the quantity of items
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]

class CartAddBookForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
