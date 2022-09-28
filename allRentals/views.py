
from urllib import response
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction
from accounts.decorators import ajax_login_required
# from .models import User

from .forms import AddVillageForm, PostImagesForm, RentalForm, VillageForm
from .models import Booked, Constituency, PostImages, UserFeedback, Village, Rental, Ward

User = get_user_model()
# Create your views here.
def home(request):
    form = RentalForm()
    context = {
        "form" : form,
    }
    return render(request,"home.html", context)

def list_rentals(request):
    if request.method == 'POST':
        selected_ward = request.POST.get('ward') #get the ward user has selected
        selected_village = request.POST.get('village') #get the village user has selected
        rentals = Rental.objects.filter(ward=selected_ward, village=selected_village) #filter display by ward & village

        booking = []
        book_pending = []
        book_accepted = []
        if rentals:                                 #if rentals with given parameters exist
            ward_name = rentals[0].ward             #get ward name for the first rental
            village_name = rentals[0].village       #get village name

            if request.user.is_authenticated:
                bookings = Booked.objects.filter(user=request.user) #retrieve all rentals current user has booked
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print(rentals)
                print(bookings)

                

                if bookings: 
                    print(bookings) #for debugging purpose

                    """ We need to check if in current retrived rentals,
                        there are those the current user has booked,
                        if so - check whether the booked rentals are still pending,
                        are accepted by landlord or are objects that were booked but later
                        canceled i.e. not pending and not booked
                        --if so, then, pass those rentals to template as a list called booking,
                        pass pending rentals as book_pending and accepted as book_accepted """

                    [booking.append(b.rental) for b in bookings]

                    for rental in rentals:
                        for b in bookings:
                            if b.is_pending and b.booked==False:
                                if b.rental == rental:
                                    print(rental)
                                    book_pending.append(rental)
                            elif b.is_pending==False and b.booked==True:
                                if b.rental == rental:
                                    print(rental)
                                    book_accepted.append(rental)
                            else:
                                pass            #or rather, pass an empty list
                    print(booking)
                    print(book_pending)
                    print(book_accepted)
            

        else: #if rentals with selected village does not exist
            ward_name = 'empty'
            village_name = 'empty'
            

        context = {
            'rentals':rentals,
            'ward_name': ward_name,
            'village_name': village_name,
            'booking': booking,
            'book_pending': book_pending,
            'book_accepted': book_accepted,
        }
    else:
        context ={}
    return render(request,'allRentals/list_rentals.html', context)

@ajax_login_required
@login_required(login_url='accounts:login')
def book(request, id):
    print(request.user)
    if request.method=='POST':
        user = request.user
        rental_id = request.POST.get('rental_id')
        r = Rental.objects.get(pk=rental_id)

        print('##################')
        print('user -- ',user)
        print('rental id ---',rental_id)
        print("renta---- ",r)
        print('##################')
        
        try:
            obj = Booked.objects.get(rental=r, user=user)
            obj.rental = r
            obj.user = user
            obj.is_pending = True
            obj.booked = False
            obj.save()
        except Booked.DoesNotExist:
            obj = Booked()
            obj.rental = r
            obj.user = user
            obj.is_pending = True
            obj.booked = False
            print('>>>>>>>>>>>>>>>>>>>>>>')
            print(obj.rental)
            print(obj.user)
            print('is_pending --- ',obj.is_pending)
            print('is_booked --- ',obj.booked)
            print(obj)
            print('>>>>>>>>>>>>>>>>>>>>>>')
            obj.save()
    # return HttpResponseRedirect(request.path)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def bookCancel(request, id):
    if request.method == 'POST':
        rental_id = request.POST.get('rental_id')
        user = request.user
        r = Rental.objects.get(pk=rental_id)

        print('##################')
        print('user -- ',user)
        print('rental id ---',rental_id)
        

        obj = Booked.objects.get(rental=r, user=user)
        print('##################')
        print(obj)
        obj.delete()
        print('--------------')
        print('object deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    
@login_required(login_url='accounts:login')
def add_rental(request):
    if request.method == 'POST':
        form = RentalForm(request.POST, request.FILES)
        images_form = PostImagesForm(request.POST, request.FILES)

        files = request.FILES.getlist('imgs')

        if form.is_valid() and images_form.is_valid():
            instance = form.save(commit=False)
            instance.landlord = request.user #=====> Get currently logged in user
            user_change = User.objects.get(pk=request.user.id) #====> Get the user's id
            user_change.is_landlord = True #=====> Set landlord true since he is adding a rental
            user_change.is_tenant = False #======> set tenant false
            user_change.save() #save changes to user
            instance.save() #save form

            for each_image in files:
                image = PostImages() #assign PostImages model to images
                image.rental_id = instance.id #get the rental_id the image belongs to
                image.imgs = each_image #get image property, i.e name and path(optional, can be ignored for security resons)
                image.save()
            return redirect('allRentals:list_rentals')
    else:
        form = RentalForm()
        images_form = PostImagesForm()

        # add_village_data = request.get(id='')
    context = {
        'rental_form':form,
        'images_form': images_form,
    }
    return render(request, 'allRentals/add_rental.html', context)

def load_wards(request):
    constituency_id = request.GET.get('constituency')
    wards = Ward.objects.filter(constituency_id=constituency_id).order_by('name')
    context = {
        'wards' : wards,
    }
    return render(request, 'allRentals/dropdownlist.html', context)


class VillageCreateView(CreateView):
    model = Village
    form_class = VillageForm
    success_url = reverse_lazy('allRentals:add_rental')

def rental_details(request, id=None):
    obj = get_object_or_404(Rental, id=id)
    images = PostImages.objects.filter(rental=obj)
    feedback = UserFeedback.objects.filter(rental=obj)
   
    context ={
        "rental": obj,
        "rental_images": images,
        "feedback": feedback,
    }
    return render(request, 'allRentals/rental_details.html', context)

@ajax_login_required
@login_required(login_url='accounts:login')
@transaction.atomic
def add_feedback(request, id):
    if request.method =='POST':
        rental_id = request.POST.get('rental_id')
        val = request.POST.get('score')
        user_msg = request.POST.get('user_msg')
        user = request.user

        try:
            r = Rental.objects.get(pk=rental_id)
            obj = UserFeedback.objects.get(rental=r, user=user)
            obj.score = val
            obj.user_msg = user_msg
            obj.user = user

            total_score = int(obj.rental.total_rating_score)
            new_score = total_score + int(obj.score)
            avg_score = (new_score//2)
            total_score = avg_score

            r.total_rating_score = total_score
            r.avg_rating_score = avg_score

            r.save()
            obj.save()

        except UserFeedback.DoesNotExist:
            obj = UserFeedback()

            obj.rental = get_object_or_404(Rental, id=rental_id)
            obj.score = val
            obj.user_msg = user_msg
            obj.user = user

            total_score = int(obj.rental.total_rating_score)
            new_score = total_score + int(obj.score)
            avg_score = (new_score//2)
            total_score = avg_score

            r = Rental.objects.get(pk=rental_id)
            
            r.total_rating_score = total_score
            r.avg_rating_score = avg_score
            

            print('>>>>>>>>>>>>>>>>>>>')
            print("rental is -- ",obj.rental)
            print("Village is -- ",obj.rental.village)
            print("User has rated is -- ",obj.score, "stars")
            print("Total rating is -- ",r.total_rating_score)
            print("Average rating is -- ",r.avg_rating_score)
            print("The message is -- ",obj.user_msg)
            print("User email is -- ",obj.user.email)
            print('>>>>>>>>>>>>>>>>>>>')
            
            r.save()
            obj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class RentalUpdateView(UpdateView):
    model = Rental
    form_class = RentalForm
    success_url = reverse_lazy('rental_list')

