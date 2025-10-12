from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from .models import User, LocalGuide


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('first_name', css_class='form-control'), css_class='col-md-6'),
                Column(Field('last_name', css_class='form-control'), css_class='col-md-6'),
            ),
            Field('username', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('password1', css_class='form-control'),
            Field('password2', css_class='form-control'),
            Submit('submit', 'Sign Up', css_class='btn btn-primary w-100')
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'profile_picture', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('first_name', css_class='form-control'), css_class='col-md-6'),
                Column(Field('last_name', css_class='form-control'), css_class='col-md-6'),
            ),
            Field('email', css_class='form-control'),
            Field('phone', css_class='form-control'),
            Field('date_of_birth', css_class='form-control'),
            Field('profile_picture', css_class='form-control'),
            Submit('submit', 'Update Profile', css_class='btn btn-primary')
        )


# Fixed Admin-only form for creating/updating guides
class LocalGuideForm(forms.ModelForm):
    user_username = forms.CharField(max_length=150, label='Username')
    user_email = forms.EmailField(label='Email')
    user_first_name = forms.CharField(max_length=30, label='First Name')
    user_last_name = forms.CharField(max_length=30, label='Last Name')

    class Meta:
        model = LocalGuide
        fields = ['region', 'description', 'experience_years', 'languages',
                  'hourly_rate', 'phone', 'guide_photo', 'references']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'references': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre-populate user fields if editing (only if instance has a user)
        if self.instance and self.instance.pk and hasattr(self.instance, 'user') and self.instance.user:
            self.fields['user_username'].initial = self.instance.user.username
            self.fields['user_email'].initial = self.instance.user.email
            self.fields['user_first_name'].initial = self.instance.user.first_name
            self.fields['user_last_name'].initial = self.instance.user.last_name

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('user_first_name', css_class='form-control'), css_class='col-md-6'),
                Column(Field('user_last_name', css_class='form-control'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('user_username', css_class='form-control'), css_class='col-md-6'),
                Column(Field('user_email', css_class='form-control'), css_class='col-md-6'),
            ),
            Field('region', css_class='form-control'),
            Field('description', css_class='form-control'),
            Row(
                Column(Field('experience_years', css_class='form-control'), css_class='col-md-6'),
                Column(Field('hourly_rate', css_class='form-control'), css_class='col-md-6'),
            ),
            Field('languages', css_class='form-control'),
            Field('phone', css_class='form-control'),
            Field('guide_photo', css_class='form-control'),
            Field('references', css_class='form-control'),
            Submit('submit', 'Save Guide', css_class='btn btn-primary')
        )

    def clean_user_username(self):
        username = self.cleaned_data['user_username']
        # Check if username exists for other users (not current one being edited)
        existing_user = User.objects.filter(username=username).first()

        # For new guide creation
        if not self.instance.pk:
            if existing_user:
                raise forms.ValidationError("This username is already taken.")
        # For editing existing guide
        else:
            if existing_user and hasattr(self.instance, 'user') and existing_user != self.instance.user:
                raise forms.ValidationError("This username is already taken.")

        return username

    def clean_user_email(self):
        email = self.cleaned_data['user_email']
        # Check if email exists for other users (not current one being edited)
        existing_user = User.objects.filter(email=email).first()

        # For new guide creation
        if not self.instance.pk:
            if existing_user:
                raise forms.ValidationError("This email is already registered.")
        # For editing existing guide
        else:
            if existing_user and hasattr(self.instance, 'user') and existing_user != self.instance.user:
                raise forms.ValidationError("This email is already registered.")

        return email