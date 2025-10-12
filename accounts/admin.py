from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, LocalGuide

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'profile_picture', 'date_of_birth')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('email', 'first_name', 'last_name')}),
    )

@admin.register(LocalGuide)
class LocalGuideAdmin(admin.ModelAdmin):
    list_display = ['user', 'region', 'experience_years', 'hourly_rate', 'rating', 'is_verified']
    list_filter = ['is_verified', 'experience_years', 'region']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'region']
    actions = ['verify_guides', 'unverify_guides']
    
    def verify_guides(self, request, queryset):
        queryset.update(is_verified=True)
    verify_guides.short_description = "Verify selected guides"
    
    def unverify_guides(self, request, queryset):
        queryset.update(is_verified=False)
    unverify_guides.short_description = "Unverify selected guides"

admin.site.register(User, CustomUserAdmin)