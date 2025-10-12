from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class LocalGuide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=200)
    description = models.TextField()
    experience_years = models.IntegerField()
    languages = models.CharField(max_length=200)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    phone = models.CharField(max_length=15)
    guide_photo = models.ImageField(upload_to='guide_photos/', blank=True, null=True)  # Updated
    references = models.TextField(blank=True)
    is_verified = models.BooleanField(default=True)  # Auto-verified since admin creates
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.region}"