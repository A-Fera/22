from django.contrib import admin
from .models import Destination, Photo, DestinationFeature

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'state', 'is_featured', 'created_at']
    list_filter = ['category', 'state', 'is_featured', 'created_at']
    search_fields = ['name', 'location', 'state', 'description']
    actions = ['make_featured', 'remove_featured']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Mark selected destinations as featured"
    
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
    remove_featured.short_description = "Remove featured status"

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['destination', 'caption', 'uploaded_by', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at', 'destination']
    search_fields = ['destination__name', 'caption']

@admin.register(DestinationFeature)
class DestinationFeatureAdmin(admin.ModelAdmin):
    list_display = ['destination', 'feature_name']
    list_filter = ['destination']