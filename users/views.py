from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UpdateUserForm, UpdateProfileForm, NewAddressForm, UpdateAddressForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import Address


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully. Please proceed to login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Profile changes saved successfully!')
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Password changed successfully!')
            return redirect('profile')
        else:
            messages.error(request, f'Unsuccessful! Please try again.')
            return redirect('profile')

    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form
        })


def address(request):
    model = Address
    queryset = model.objects.filter(address_user=request.user)
    context = {
        'my-addresses': queryset
    }
    return render(request, 'shipping_addresses.html', context=context)


@login_required
def address_add(request):
    if request.method == 'POST':
        add_form = NewAddressForm(request.POST, instnace=request.address)
        if add_form.is_valid():
            add_form.save()
            messages.success(request, f'Address added successfully!')
            return redirect('shipping_addresses')
    else:
        add_form = NewAddressForm()
    return render(request, 'shipping_addresses_add.html', {'add_form': add_form})


@login_required
def address_edit(request):
    if request.method == 'POST':
        edit_form = UpdateAddressForm(request.POST, instance=request.address)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, f'Address changes saved successfully!')
            return redirect('shipping_addresses')
        else:
            edit_form = NewAddressForm()
    return render(request, 'shipping_addresses_add.html', {'edit_form': edit_form})


@login_required
def address_delete(request, address_id):
    if request.method == 'GET':
        address = get_object_or_404(Address, id=address_id)
        address.delete()
        messages.success(request, f'Address removed successfully!')
        return redirect('shipping_addresses')
