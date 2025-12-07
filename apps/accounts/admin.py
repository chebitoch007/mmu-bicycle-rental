from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PenaltyLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom user admin with verification and penalty management
    """
    list_display = ['username', 'university_id', 'email', 'role', 'is_verified', 'is_active_renter', 'penalties']
    list_filter = ['role', 'is_verified', 'is_active_renter', 'is_staff']
    search_fields = ['username', 'email', 'university_id', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('University Info', {
            'fields': ('university_id', 'university_id_document', 'role')
        }),
        ('Contact', {
            'fields': ('phone_number', 'date_of_birth', 'address')
        }),
        ('Account Status', {
            'fields': ('is_verified', 'is_active_renter', 'penalties', 'profile_picture')
        }),
    )
    
    actions = ['verify_users', 'suspend_users', 'activate_users']
    
    def verify_users(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} users verified successfully.')
    verify_users.short_description = "Verify selected users"
    
    def suspend_users(self, request, queryset):
        updated = queryset.update(is_active_renter=False)
        self.message_user(request, f'{updated} users suspended from renting.')
    suspend_users.short_description = "Suspend selected users"
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active_renter=True)
        self.message_user(request, f'{updated} users activated for renting.')
    activate_users.short_description = "Activate selected users"


@admin.register(PenaltyLog)
class PenaltyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'reason', 'created_at', 'resolved', 'resolved_by']
    list_filter = ['resolved', 'created_at']
    search_fields = ['user__username', 'reason']
    readonly_fields = ['created_at']
    
    def save_model(self, request, obj, form, change):
        if obj.resolved and not obj.resolved_by:
            obj.resolved_by = request.user
        super().save_model(request, obj, form, change)