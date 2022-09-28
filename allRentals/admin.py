from django.contrib import admin
from .models import Constituency, UserFeedback, Ward, Village, Rental,PostImages, Booked, Favorite

# Register your models here.
class PostImagesAdmin(admin.StackedInline):
    model = PostImages
    # we are using StackedInline class to edit “PostImages” model inside “Hostel” model.

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    inlines = [PostImagesAdmin]

    class Meta:
        model = Rental

@admin.register(PostImages)
class PostImagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Constituency)
admin.site.register(Ward)
admin.site.register(Village)
admin.site.register(UserFeedback)
admin.site.register(Booked)
admin.site.register(Favorite)
