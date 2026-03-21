from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # Display more columns in the list view
    list_display = ('name', 'specialization', 'experience_years', 'contact_number', 'is_available')
    
    # Add filters for specialization and availability
    list_filter = ('specialization', 'is_available')
    
    # Enable searching for name and specialization
    search_fields = ('name', 'specialization')
    
    # Organize fields into sections in the detail view
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'specialization', 'experience_years')
        }),
        ('Contact Details', {
            'fields': ('contact_number', 'email')
        }),
        ('Status', {
            'fields': ('is_available',)
        }),
    )
    
    # Make the experience_years field easier to edit
    list_editable = ('is_available',)
