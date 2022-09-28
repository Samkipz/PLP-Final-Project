from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, LandlordProfile, TenantProfile


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name','last_name','email', 'phone_no')

class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ('email', 'phone_no')



