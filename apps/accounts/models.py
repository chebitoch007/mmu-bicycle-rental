from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from core.validators import validate_file_size


class User(AbstractUser):
    """
    Custom user model for MMU Bicycle Rental System
    Supports both students and staff with role-based access
    """
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    
    # Basic Info
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        blank=True,
        null=True
    )
    
    # University Info
    university_id = models.CharField(
        max_length=20,
        unique=True,
        help_text="MMU Student/Staff ID"
    )
    university_id_document = models.ImageField(
        upload_to='university_ids/',
        validators=[validate_file_size],
        help_text="Upload a clear photo of your University ID",
        blank=True,
        null=True
    )
    
    # Profile
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        validators=[validate_file_size],
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    
    # Account Status
    is_verified = models.BooleanField(
        default=False,
        help_text="Verified by admin after ID check"
    )
    is_active_renter = models.BooleanField(
        default=True,
        help_text="Can rent bicycles"
    )
    penalties = models.IntegerField(
        default=0,
        help_text="Number of penalties incurred"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['university_id']),
            models.Index(fields=['role', 'is_verified']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.university_id})"
    
    @property
    def has_active_rental(self):
        """Check if user has an active rental"""
        return self.rentals.filter(status='active').exists()
    
    @property
    def has_active_reservation(self):
        """Check if user has an active reservation"""
        from apps.rentals.models import Reservation
        return Reservation.objects.filter(
            user=self,
            status='active'
        ).exists()
    
    @property
    def can_rent(self):
        """Check if user can rent a bicycle"""
        return (
            self.is_verified and 
            self.is_active_renter and 
            not self.has_active_rental and
            self.penalties < 3  # Max 3 penalties before suspension
        )
    
    def add_penalty(self, reason=""):
        """Add a penalty to the user"""
        self.penalties += 1
        if self.penalties >= 3:
            self.is_active_renter = False
        self.save()
        
        # Log penalty
        PenaltyLog.objects.create(
            user=self,
            reason=reason
        )
    
    def get_total_rentals(self):
        """Get total number of completed rentals"""
        return self.rentals.filter(status='completed').count()


class PenaltyLog(models.Model):
    """Track user penalties"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='penalty_logs')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='resolved_penalties'
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Penalty for {self.user.username} - {self.created_at.date()}"