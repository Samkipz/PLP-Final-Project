from django.urls import path

from . import views

app_name = 'allRentals'

urlpatterns = [
    path('', views.home, name='home'),
    path('addRentals/', views.add_rental, name='add_rental'),
    path('addRentals/add', views.VillageCreateView.as_view(), name='village_add'),
    path('allRentals/', views.list_rentals, name='list_rentals'),
    path("book/<int:id>", views.book, name="book"),
    path("bookCancel/<int:id>", views.bookCancel, name="bookCancel"),
    path('<int:id>/', views.rental_details, name='rental_details'),
    path('<int:id>/add_feedback', views.add_feedback, name='add_feedback'),
    path('<int:pk>/', views.RentalUpdateView.as_view(), name='rental_change'),

    path('ajax/load-wards/', views.load_wards, name='ajax_load_wards'),
] 