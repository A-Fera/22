from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import Accommodation, Booking

class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = [
            'name', 'accommodation_type', 'destination', 'address', 'description',
            'amenities', 'price_per_night', 'max_guests', 'phone', 'email',
            'website', 'image', 'check_in_time', 'check_out_time'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'amenities': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('accommodation_type', css_class='form-select'),
            Field('destination', css_class='form-select'),
            Field('address', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('amenities', css_class='form-control'),
            Field('price_per_night', css_class='form-control'),
            Field('max_guests', css_class='form-control'),
            Field('phone', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('website', css_class='form-control'),
            Field('image', css_class='form-control'),
            Field('check_in_time', css_class='form-control'),
            Field('check_out_time', css_class='form-control'),
            Submit('submit', 'Save Accommodation', css_class='btn btn-primary')
        )

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'number_of_guests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('check_in_date', css_class='form-control'),
            Field('check_out_date', css_class='form-control'),
            Field('number_of_guests', css_class='form-control'),
            Submit('submit', 'Book Now', css_class='btn btn-primary')
        )