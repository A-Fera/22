from django.contrib import admin
from .models import Itinerary, ItineraryItem, ItineraryCollaborator

class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 1
    fields = ['item_type', 'title', 'destination', 'start_date', 'end_date', 'estimated_cost', 'is_booked']

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'start_date', 'end_date', 'status', 'is_public', 'created_at']
    list_filter = ['status', 'is_public', 'start_date', 'created_at']
    search_fields = ['title', 'user__username', 'description']
    inlines = [ItineraryItemInline]
    date_hierarchy = 'start_date'

@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'itinerary', 'item_type', 'start_date', 'end_date', 'estimated_cost', 'is_booked']
    list_filter = ['item_type', 'is_booked', 'start_date']
    search_fields = ['title', 'itinerary__title', 'description']

@admin.register(ItineraryCollaborator)
class ItineraryCollaboratorAdmin(admin.ModelAdmin):
    list_display = ['itinerary', 'user', 'permission', 'invited_at', 'accepted_at']
    list_filter = ['permission', 'invited_at']