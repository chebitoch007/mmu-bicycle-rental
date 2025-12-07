from django.contrib import admin
from .models import Reservation, Rental


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bicycle', 'station', 'status', 'created_at', 'expires_at']
    list_filter = ['status', 'created_at', 'station']
    search_fields = ['user__username', 'bicycle__serial_number']
    readonly_fields = ['created_at', 'picked_up_at', 'cancelled_at']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'bicycle', 'station', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at', 'picked_up_at', 'cancelled_at')
        }),
    )
    
    actions = ['expire_reservations', 'cancel_reservations']
    
    def expire_reservations(self, request, queryset):
        count = 0
        for reservation in queryset.filter(status='active'):
            reservation.expire()
            count += 1
        self.message_user(request, f'{count} reservations expired.')
    expire_reservations.short_description = "Expire selected reservations"
    
    def cancel_reservations(self, request, queryset):
        count = 0
        for reservation in queryset.filter(status='active'):
            reservation.cancel()
            count += 1
        self.message_user(request, f'{count} reservations cancelled.')
    cancel_reservations.short_description = "Cancel selected reservations"


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bicycle', 'status', 'start_time', 'end_time', 'total_cost']
    list_filter = ['status', 'start_time', 'pickup_station', 'return_station']
    search_fields = ['user__username', 'bicycle__serial_number']
    readonly_fields = ['start_time', 'hourly_rate']
    
    fieldsets = (
        ('Rental Info', {
            'fields': ('user', 'bicycle', 'reservation', 'status')
        }),
        ('Stations', {
            'fields': ('pickup_station', 'return_station')
        }),
        ('Timestamps', {
            'fields': ('start_time', 'end_time')
        }),
        ('Cost', {
            'fields': ('hourly_rate', 'total_cost', 'late_fee', 'damage_fee')
        }),
        ('Notes', {
            'fields': ('pickup_notes', 'return_notes', 'distance_km')
        }),
    )
    
    actions = ['complete_rentals', 'calculate_costs']
    
    def complete_rentals(self, request, queryset):
        count = 0
        for rental in queryset.filter(status='active'):
            rental.complete_rental(
                return_station=rental.pickup_station,
                return_notes='Completed by admin'
            )
            count += 1
        self.message_user(request, f'{count} rentals completed.')
    complete_rentals.short_description = "Complete selected rentals"
    
    def calculate_costs(self, request, queryset):
        for rental in queryset:
            rental.calculate_cost()
            rental.save()
        self.message_user(request, f'Costs recalculated for {queryset.count()} rentals.')
    calculate_costs.short_description = "Recalculate costs"