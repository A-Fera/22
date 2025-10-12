from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from .models import DestinationReview, AccommodationReview, ReviewPhoto

class DestinationReviewForm(forms.ModelForm):
    class Meta:
        model = DestinationReview
        fields = ['title', 'content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control'),
            Field('rating', css_class='form-select'),
            Field('content', css_class='form-control'),
            Submit('submit', 'Submit Review', css_class='btn btn-primary')
        )

class AccommodationReviewForm(forms.ModelForm):
    class Meta:
        model = AccommodationReview
        fields = ['title', 'content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control'),
            Field('rating', css_class='form-select'),
            Field('content', css_class='form-control'),
            Submit('submit', 'Submit Review', css_class='btn btn-primary')
        )

class ReviewPhotoForm(forms.ModelForm):
    class Meta:
        model = ReviewPhoto
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('image', css_class='form-control'),
            Field('caption', css_class='form-control'),
            Submit('submit', 'Upload Photo', css_class='btn btn-primary')
        )

# Multiple photo upload formset
ReviewPhotoFormSet = forms.modelformset_factory(
    ReviewPhoto,
    form=ReviewPhotoForm,
    extra=3,
    max_num=5,
    can_delete=True
)