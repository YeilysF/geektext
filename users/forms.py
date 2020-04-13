from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'account_nickname', 'first_name', 'middle_name', 'last_name']