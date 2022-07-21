from django import forms
from django.forms import ModelForm
from .models import Venue

class VenueForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Venue
        fields = '__all__'

    def clean(self):
        cleaned_date = super().clean()
        phone = cleaned_date.get("phone")
        email_address = cleaned_date.get("email_address")
        if not  (phone or email_address):
            raise forms.ValidationError(
                "You must enter either a phone number or an email, or both."
            )