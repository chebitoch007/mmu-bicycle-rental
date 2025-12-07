from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User
from apps.bicycles.models import Bicycle
from apps.stations.models import Station


class ReservationManager(models.Manager):
    """Custom manager for Reservation queries"""
    
    def active(self):
        """Get active reservations"""
        return self.filter(status='active')
    
    def expired(self):
        """Get expired reservations"""
        return self.filter(status='expired')
    
    def check_and_expire(self):
        """Check and expire reservations past 30 minutes"""
        expiry_time = timezone.now() - timedelta(minutes=30)
        expired = self.filter(
            status='active',
            created_at__lt=expiry_time
        )
        
        for reservation in expired:
            reservation.expire()
        
        return expired.count()


class Reservation(models.Model):
    """
    Bicycle reservation model
    Reservations expire after 30 minutes if not picked up
    """
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('picked-up', 'Picked Up'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE, related_name='reservations')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='reservations')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    picked_up_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    
    objects = ReservationManager()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['bicycle', 'status']),
            models.Index(fields=['status', 'expires_at']),
        ]
    
    def __str__(self):
        return f"Reservation #{self.id} - {self.user.username} - {self.bicycle.serial_number}"
    
    def save(self, *args, **kwargs):
        """Auto-set expiry time if not set"""
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        """Check if reservation is still active"""
        return self.status == 'active' and timezone.now() < self.expires_at
    
    @property
    def is_expired(self):
        """Check if reservation has expired"""
        return timezone.now() >= self.expires_at and self.status == 'active'
    
    @property
    def time_remaining(self):
        """Get time remaining in seconds"""
        if self.status != 'active':
            return 0
        remaining = (self.expires_at - timezone.now()).total_seconds()
        return max(0, remaining)
    
    def expire(self):
        """Mark reservation as expired"""
        self.status = 'expired'
        self.save()
        
        # Make bicycle available again
        self.bicycle.mark_as_available()
    
    def cancel(self):
        """Cancel the reservation"""
        self.status = 'cancelled'
        self.cancelled_at = timezone.now()
        self.save()
        
        # Make bicycle available again
        self.bicycle.mark_as_available()
    
    def convert_to_rental(self):
        """Convert reservation to rental"""
        self.status = 'picked-up'
        self.picked_up_at = timezone.now()
        self.save()


class RentalManager(models.Manager):
    """Custom manager for Rental queries"""
    
    def active(self):
        """Get active rentals"""
        return self.filter(status='active')
    
    def completed(self):
        """Get completed rentals"""
        return self.filter(status='completed')
    
    def overdue(self):
        """Get overdue rentals (active for more than 24 hours)"""
        overdue_time = timezone.now() - timedelta(hours=24)
        return self.filter(
            status='active',
            start_time__lt=overdue_time
        )


class Rental(models.Model):
    """
    Bicycle rental model
    Tracks active and completed rentals
    """
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE, related_name='rentals')
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='rental'
    )
    
    # Stations
    pickup_station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name='pickup_rentals'
    )
    return_station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name='return_rentals',
        blank=True,
        null=True
    )
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Timestamps
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    
    # Cost calculation
    hourly_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Rate at time of rental"
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Additional charges
    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    damage_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Notes
    pickup_notes = models.TextField(blank=True, help_text="Condition at pickup")
    return_notes = models.TextField(blank=True, help_text="Condition at return")
    
    # Distance tracking
    distance_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text="Distance traveled in KM"
    )
    
    objects = RentalManager()
    
    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['bicycle', 'status']),
            models.Index(fields=['status', 'start_time']),
        ]
    
    def __str__(self):
        return f"Rental #{self.id} - {self.user.username} - {self.bicycle.serial_number}"
    
    def save(self, *args, **kwargs):
        """Set hourly rate from bicycle if not set"""
        if not self.hourly_rate:
            self.hourly_rate = self.bicycle.hourly_rate
        super().save(*args, **kwargs)
    
    @property
    def duration(self):
        """Calculate rental duration"""
        if self.status == 'active':
            return timezone.now() - self.start_time
        elif self.end_time:
            return self.end_time - self.start_time
        return timedelta(0)
    
    @property
    def duration_hours(self):
        """Get duration in hours (decimal)"""
        total_seconds = self.duration.total_seconds()
        return total_seconds / 3600
    
    @property
    def is_overdue(self):
        """Check if rental is overdue (more than 24 hours)"""
        return self.status == 'active' and self.duration_hours > 24
    
    def calculate_cost(self):
        """Calculate total rental cost"""
        hours = self.duration_hours
        
        # Base cost
        base_cost = self.hourly_rate * hours
        
        # Late fee (after 24 hours, 50% extra per hour)
        if hours > 24:
            overtime_hours = hours - 24
            self.late_fee = self.hourly_rate * overtime_hours * 0.5
        
        # Total cost
        self.total_cost = base_cost + self.late_fee + self.damage_fee
        
        return self.total_cost
    
    def complete_rental(self, return_station, return_notes="", distance_km=0):
        """Complete the rental"""
        self.end_time = timezone.now()
        self.return_station = return_station
        self.return_notes = return_notes
        self.distance_km = distance_km
        self.status = 'completed'
        
        # Calculate final cost
        self.calculate_cost()
        self.save()
        
        # Update bicycle
        self.bicycle.mark_as_available()
        self.bicycle.current_station = return_station
        self.bicycle.increment_rental_count()
        self.bicycle.total_distance_km += distance_km
        self.bicycle.save()
        
        # Check for late penalty
        if self.is_overdue:
            self.user.add_penalty(f"Late return of rental #{self.id}")
    
    def cancel_rental(self):
        """Cancel the rental"""
        self.status = 'cancelled'
        self.end_time = timezone.now()
        self.save()
        
        # Make bicycle available
        self.bicycle.mark_as_available()