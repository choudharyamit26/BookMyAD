from django import forms
from .models import Category, City, Publication, AdType, Ad
from django.forms import CheckboxSelectMultiple

# class PersonForm(forms.ModelForm):
#     class Meta:
#         model = Person
#         fields = ('name', 'birthdate', 'country', 'city')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['city'].queryset = City.objects.none()
#
#         if 'country' in self.data:
#             try:
#                 country_id = int(self.data.get('country'))
#                 self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty City queryset
#         elif self.instance.pk:
#             self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
CHOICES = [('pi', 'PI'), ('ci', 'CI')]


class AdForm(forms.ModelForm):
    # city = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=City.objects.all())
    # city = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
    #                                  label="Notify and subscribe users to this post:")

    # publication = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=Publication.objects.all())

    class Meta:
        model = AdType
        fields = ('category', 'city', 'publication', 'ad')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publication'].queryset = Publication.objects.none()
        self.fields['ad'].queryset = Ad.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['city'].queryset = Publication.objects.filter(city=city_id).order_by('city')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.city.publication_set.order_by('city')

        if 'publication' in self.data:
            try:
                publication_id = int(self.data.get('publication'))
                self.fields['publication'].queryset = Ad.objects.filter(publication=publication_id).order_by(
                    'publication')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['publication'].queryset = self.instance.publication.ad_set.order_by('publication')
