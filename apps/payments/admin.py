from django.contrib import admin
from .models import Payment, Refund


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'rental', 'method', 'amount', 'status', 'created_at']
    list_filter = ['method', 'status', 'created_at']
    search_fields = ['user__username', 'transaction_id', 'reference_number']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('Payment Info', {
            'fields': ('user', 'rental', 'method', 'amount', 'status')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'reference_number', 'provider_response')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )
    
    actions = ['mark_completed', 'mark_failed']
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} payments marked as completed.')
    mark_completed.short_description = "Mark as Completed"
    
    def mark_failed(self, request, queryset):
        updated = queryset.update(status='failed')
        self.message_user(request, f'{updated} payments marked as failed.')
    mark_failed.short_description = "Mark as Failed"


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'amount', 'status', 'requested_at']
    list_filter = ['status', 'requested_at']
    search_fields = ['payment__transaction_id', 'reason']
    readonly_fields = ['requested_at', 'processed_at']