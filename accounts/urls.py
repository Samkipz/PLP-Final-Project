from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('landlordprofile/', views.landlordprofile, name='landlordprofile'),
    path("userProfile/<int:id>", views.userProfile, name="userProfile"),
]