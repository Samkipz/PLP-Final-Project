from django import forms
from .models import PostImages, Rental, Village, Ward
from django.utils.translation import gettext_lazy as _

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ('name', 'rent', 'constituency', 'ward', 'village', 'availability', 'content', 'img')

        labels = {
            'name' : _('Rental Name'),
            'rent' : _('Monthly rent per room in Ksh'),
            'constituency' : _('Select constituency'),
            'ward' : _('Select ward'),
            'village' : _('Select village'),
            'availability' : _('Rooms available for rent'),
            'content' : _('Rentals Description'),
            'img' : _('Upload an image of the rentals')
        }

class PostImagesForm(forms.ModelForm):
    class Meta:
        model = PostImages
        fields = ['imgs']
        widgets = {
            'imgs': forms.FileInput(attrs={'id': 'myfile', 'class': 'form-control-file', 'multiple': True}),
        }
        labels = {
            'imgs' : _('Add Other Images'),
        }

class AddVillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ('constituency','ward', 'name')

        labels = {
            'constituency' : _('Select constituency'),
            'ward' : _('Select ward'),
            'name' : _('Village Name')
        }

class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ('constituency','ward', 'name')

        labels = {
            'constituency' : _('Select constituency'),
            'ward' : _('Select ward'),
            'name' : _('Village Name')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ward'].queryset = Ward.objects.none()

        if 'constituency' in self.data:
            try:
                constituency_id = int(self.data.get('constituency'))
                self.fields['ward'].queryset = Ward.objects.filter(constituency_id=constituency_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Ward queryset
        elif self.instance.pk:
            self.fields['ward'].queryset = self.instance.constituency.ward_set.order_by('name')


