from django.contrib import admin
from .models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'address', 'capacity', 'available_bikes_count', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'address']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Location', {
            'fields': ('address', 'latitude', 'longitude')
        }),
        ('Capacity', {
            'fields': ('capacity', 'operating_hours')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def available_bikes_count(self, obj):
        return obj.available_bikes_count
    available_bikes_count.short_description = 'Available Bikes'