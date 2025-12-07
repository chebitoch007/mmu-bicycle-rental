from django.contrib import admin
from .models import Bicycle, MaintenanceLog


@admin.register(Bicycle)
class BicycleAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'status', 'condition', 'current_station', 'hourly_rate', 'total_rentals']
    list_filter = ['status', 'condition', 'current_station']
    search_fields = ['name', 'model', 'serial_number']
    readonly_fields = ['slug', 'created_at', 'updated_at', 'total_rentals', 'total_distance_km']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model', 'manufacturer', 'serial_number', 'slug')
        }),
        ('Description', {
            'fields': ('description', 'image')
        }),
        ('Specifications', {
            'fields': ('frame_size', 'color', 'gear_count')
        }),
        ('Pricing', {
            'fields': ('hourly_rate',)
        }),
        ('Status & Location', {
            'fields': ('status', 'condition', 'current_station')
        }),
        ('Tracking', {
            'fields': ('total_rentals', 'total_distance_km', 'last_maintenance_date', 'next_maintenance_date')
        }),
        ('Metadata', {
            'fields': ('purchase_date', 'purchase_price', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_available', 'mark_maintenance', 'mark_retired']
    
    def mark_available(self, request, queryset):
        updated = queryset.update(status='available')
        self.message_user(request, f'{updated} bicycles marked as available.')
    mark_available.short_description = "Mark as Available"
    
    def mark_maintenance(self, request, queryset):
        updated = queryset.update(status='maintenance')
        self.message_user(request, f'{updated} bicycles marked for maintenance.')
    mark_maintenance.short_description = "Mark for Maintenance"
    
    def mark_retired(self, request, queryset):
        updated = queryset.update(status='retired')
        self.message_user(request, f'{updated} bicycles marked as retired.')
    mark_retired.short_description = "Mark as Retired"


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ['bicycle', 'performed_at', 'cost', 'is_completed', 'performed_by']
    list_filter = ['is_completed', 'performed_at']
    search_fields = ['bicycle__serial_number', 'description']
    readonly_fields = ['performed_at']
    
    fieldsets = (
        (None, {
            'fields': ('bicycle', 'description', 'cost')
        }),
        ('Performance', {
            'fields': ('performed_by', 'performed_at', 'is_completed', 'completed_at')
        }),
    )