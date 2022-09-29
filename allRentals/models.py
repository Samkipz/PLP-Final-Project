from django.conf import settings
from smart_selects.db_fields import ChainedForeignKey
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.db import models

# Create your models here.

User = settings.AUTH_USER_MODEL

from django.db import models

class Constituency(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Ward(models.Model):
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Village(models.Model):
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True)
    # constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, null=True)
    # ward = ChainedForeignKey(
    #     Ward,
    #     chained_field="constituency",
    #     chained_model_field="constituency",
    #     show_all=False,
    #     auto_choose=True,
    #     sort=True)
    # ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Rental(models.Model):
    # slug = models.SlugField(null=False, unique=True, blank=True)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    rent = models.IntegerField()
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, null=True, default=None)
    ward = ChainedForeignKey(
        Ward,
        chained_field="constituency",
        chained_model_field="constituency",
        show_all=False,
        auto_choose=True,
        sort=True)

    village = ChainedForeignKey(
        Village,
        chained_field="ward",
        chained_model_field="ward",
        show_all=False,
        auto_choose=True,
        sort=True)

    availability = models.IntegerField()
    content = RichTextField(blank=True, null=True)
    img = models.ImageField(blank=True)
    total_rating_score = models.IntegerField(default=5)
    avg_rating_score = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class PostImages(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    imgs = models.ImageField(upload_to='pics')

    def __str__(self):
        return self.rental.name

class Booked(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    is_pending = models.BooleanField(default=False)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return 'Booking for ' + self.rental.name

class Favorite(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return 'Like for ' + self.rental.name
    
class UserFeedback(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    score = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
    user_msg = models.TextField(max_length=400, blank=True)
    feedback_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return 'feedback for ' + self.rental.name

    def get_update_url(self):
        return reverse("allRentals:rental_details", kwargs={"id": self.id})