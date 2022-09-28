from django.contrib import auth, messages
from django.shortcuts import render, redirect

from .models import TenantProfile
from . form import MyUserCreationForm


# Create your views here.
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

def profile(request):
    tenant = TenantProfile.objects.get(user=request.user)
    context = {
        'tenant': tenant,
    }
    return render(request, 'accounts/tenantprofile.html', context)