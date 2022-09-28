import os
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from allRentals.models import Rental
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(_('email address'), unique=True)
    is_landlord = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    phone_no = models.CharField(_('phone number'), max_length=15, blank=True)
    avatar = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.first_name+' '+self.last_name

    def get_avatar(self):
        if not self.avatar:
            return "/media/profile_pics/default-profile.png"
        else:
            return os.path.join(settings.MEDIA_URL, self.avatar.name)

class LandlordProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='landlord_profile')


class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='tenant_profile')
    rental = models.OneToOneField(Rental, on_delete=models.DO_NOTHING, null=True)
    is_verified = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('User profile created? >>>>>>>>>>', created)
    if instance.is_tenant:
        TenantProfile.objects.get_or_create(user = instance)
    else:
        LandlordProfile.objects.get_or_create(user = instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    print('>>>>>>>>>> User profile saved >>>>>>>>>>')
    # print(instance.tenantprofile.rental, instance.tenantprofile.date_joined)
    if instance.is_tenant:
        instance.tenant_profile.save()
    else:
        instance.landlord_profile.save()
        # LandlordProfile.objects.get_or_create(user = instance)
