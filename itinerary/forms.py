from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column, Div
from .models import Itinerary, ItineraryItem
from destinations.models import Destination
from bookings.models import Accommodation


class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['title', 'description', 'start_date', 'end_date', 'status', 'is_public']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control'),
            Field('description', css_class='form-control'),
            Row(
                Column(Field('start_date', css_class='form-control'), css_class='col-md-6'),
                Column(Field('end_date', css_class='form-control'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('status', css_class='form-select'), css_class='col-md-6'),
                Column(
                    Div(
                        Field('is_public'),
                        css_class='form-check mt-4'
                    ),
                    css_class='col-md-6'
                ),
            ),
            Submit('submit', 'Save Itinerary', css_class='btn btn-primary')
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data


class ItineraryItemForm(forms.ModelForm):
    class Meta:
        model = ItineraryItem
        fields = [
            'item_type', 'destination', 'accommodation', 'title', 'description',
            'location', 'start_date', 'end_date', 'start_time', 'end_time',
            'estimated_cost', 'notes', 'is_booked'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        self.itinerary = kwargs.pop('itinerary', None)
        super().__init__(*args, **kwargs)

        # Set date range based on itinerary
        if self.itinerary:
            self.fields['start_date'].widget.attrs.update({
                'min': self.itinerary.start_date.strftime('%Y-%m-%d'),
                'max': self.itinerary.end_date.strftime('%Y-%m-%d')
            })
            self.fields['end_date'].widget.attrs.update({
                'min': self.itinerary.start_date.strftime('%Y-%m-%d'),
                'max': self.itinerary.end_date.strftime('%Y-%m-%d')
            })

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('item_type', css_class='form-select'), css_class='col-md-6'),
                Column(Field('title', css_class='form-control'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('destination', css_class='form-select'), css_class='col-md-6'),
                Column(Field('accommodation', css_class='form-select'), css_class='col-md-6'),
            ),
            Field('description', css_class='form-control'),
            Field('location', css_class='form-control'),
            Row(
                Column(Field('start_date', css_class='form-control'), css_class='col-md-6'),
                Column(Field('end_date', css_class='form-control'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('start_time', css_class='form-control'), css_class='col-md-6'),
                Column(Field('end_time', css_class='form-control'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('estimated_cost', css_class='form-control'), css_class='col-md-6'),
                Column(
                    Div(
                        Field('is_booked'),
                        css_class='form-check mt-4'
                    ),
                    css_class='col-md-6'
                ),
            ),
            Field('notes', css_class='form-control'),
            Submit('submit', 'Save Item', css_class='btn btn-primary')
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")

        if start_date == end_date and start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time on the same day.")

        return cleaned_data


class QuickDestinationForm(forms.Form):
    destination = forms.ModelChoiceField(
        queryset=Destination.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.itinerary = kwargs.pop('itinerary', None)
        super().__init__(*args, **kwargs)

        if self.itinerary:
            self.fields['start_date'].widget.attrs.update({
                'min': self.itinerary.start_date.strftime('%Y-%m-%d'),
                'max': self.itinerary.end_date.strftime('%Y-%m-%d')
            })
            self.fields['end_date'].widget.attrs.update({
                'min': self.itinerary.start_date.strftime('%Y-%m-%d'),
                'max': self.itinerary.end_date.strftime('%Y-%m-%d')
            })