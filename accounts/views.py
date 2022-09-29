import re
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from allRentals.models import Rental, Booked
from .models import TenantProfile
from . form import MyUserCreationForm


# Create your views here.

User = get_user_model()
#Register New User
def register_view(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = MyUserCreationForm()
    return render(request, 'accounts/register.html', {'form':form})

#login user
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email", "default value")
        password = request.POST.get("password", "default value")

        user = auth.authenticate(request, email = email, password = password)

        if user is not None:
            auth.login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')
        else:
            messages.error(request,'Your Username or Password is incorrect')
    context = {}
    return render(request,'accounts/login.html', context)

def landlordprofile(request):
    return render(request, 'accounts/landlordprofile.html')

@login_required(login_url='accounts:login')
def userProfile(request, id):
    userProfile = User.objects.get(id=id)

    if userProfile.is_landlord:
        rentals = Rental.objects.filter(landlord = id)
        for r in rentals:
            total_book = Booked.objects.filter(rental = r)
        total_book = len(total_book)
    else:
        rentals = Booked.objects.filter(user=userProfile)
        total_book = len(rentals)

    context = {
        'userProfile': userProfile,
        'rentals': rentals,
        'total_book': total_book,
    }
    return render(request, 'accounts/tenantprofile.html', context)