from django.contrib import admin
from .models import Accommodation, Booking

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['name', 'accommodation_type', 'destination', 'price_per_night', 'rating', 'is_available']
    list_filter = ['accommodation_type', 'destination', 'is_available', 'created_at']
    search_fields = ['name', 'destination__name', 'address']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'accommodation', 'check_in_date', 'check_out_date', 'booking_status', 'payment_status']
    list_filter = ['booking_status', 'payment_status', 'created_at']
    search_fields = ['user__username', 'accommodation__name']