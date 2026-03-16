from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('name', 'specialty', 'email', 'phone', 'years_experience', 'is_available', 'created_at')

    # Fields to filter by in the sidebar
    list_filter = ('specialty', 'is_available', 'years_experience', 'created_at')

    # Fields to search
    search_fields = ('name', 'email', 'specialty')

    # Fields to display in the form (organize into fieldsets)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'specialty', 'email', 'phone'),
        }),
        ('Professional Details', {
            'fields': ('address', 'years_experience', 'is_available'),
            'classes': ('collapse',),  # Collapsible section
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # Make created_at read-only
    readonly_fields = ('created_at',)

    # Default ordering in admin
    ordering = ('name',)

    # Number of items per page
    list_per_page = 20

    # Actions
    actions = ['mark_as_available', 'mark_as_unavailable']

    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(request, f"{queryset.count()} doctors marked as available.")
    mark_as_available.short_description = "Mark selected doctors as available"

    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, f"{queryset.count()} doctors marked as unavailable.")
    mark_as_unavailable.short_description = "Mark selected doctors as unavailable"

