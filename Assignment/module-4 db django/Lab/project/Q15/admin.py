from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active', 'created_at')

    # Add filters on the right side
    list_filter = ('category', 'is_active', 'created_at')

    # Enable search functionality
    search_fields = ('name', 'description')

    # Fields to display in the form
    # fields = ('name', 'description', 'price', 'category', 'stock_quantity', 'is_active')

    # Make certain fields readonly
    readonly_fields = ('created_at', 'updated_at')

    # Add date hierarchy for created_at
    date_hierarchy = 'created_at'

    # Ordering in list view
    ordering = ('-created_at',)

    # Add actions
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} products marked as active.")
    make_active.short_description = "Mark selected products as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} products marked as inactive.")
    make_inactive.short_description = "Mark selected products as inactive"

    # Customize the form layout
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock_quantity', 'category')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
