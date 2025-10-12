from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import Destination, Photo

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'category', 'location', 'state', 'country',
                 'latitude', 'longitude', 'best_time_to_visit', 'entry_fee', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.NumberInput(attrs={'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'step': 'any'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('category', css_class='form-control'),
            Field('location', css_class='form-control'),
            Field('state', css_class='form-control'),
            Field('country', css_class='form-control'),
            Field('latitude', css_class='form-control'),
            Field('longitude', css_class='form-control'),
            Field('best_time_to_visit', css_class='form-control'),
            Field('entry_fee', css_class='form-control'),
            Field('is_featured'),
            Submit('submit', 'Save Destination', css_class='btn btn-primary')
        )

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'is_primary']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('image', css_class='form-control'),
            Field('caption', css_class='form-control'),
            Field('is_primary'),
            Submit('submit', 'Upload Photo', css_class='btn btn-primary')
        )