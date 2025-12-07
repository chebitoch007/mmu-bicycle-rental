from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from apps.stations.models import Station
from core.validators import validate_file_size


class BicycleManager(models.Manager):
    """Custom manager for Bicycle queries"""
    
    def available(self):
        """Get all available bicycles"""
        return self.filter(status='available')
    
    def at_station(self, station):
        """Get bicycles at a specific station"""
        return self.filter(current_station=station)
    
    def available_at_station(self, station):
        """Get available bicycles at a specific station"""
        return self.filter(status='available', current_station=station)


class Bicycle(models.Model):
    """
    Bicycle model with tracking and availability
    """
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in-use', 'In Use'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    
    # Description
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='bicycles/',
        validators=[validate_file_size],
        blank=True,
        null=True
    )
    
    # Specifications
    frame_size = models.CharField(max_length=20, blank=True, help_text="e.g., M, L, XL")
    color = models.CharField(max_length=50, blank=True)
    gear_count = models.PositiveIntegerField(default=1, help_text="Number of gears")
    
    # Pricing
    hourly_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=50.00,
        help_text="Hourly rental rate in KES"
    )
    
    # Status & Location
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    current_station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name='bicycles'
    )
    
    # Tracking
    total_rentals = models.PositiveIntegerField(default=0)
    total_distance_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Total distance traveled in KM"
    )
    last_maintenance_date = models.DateField(blank=True, null=True)
    next_maintenance_date = models.DateField(blank=True, null=True)
    
    # Metadata
    purchase_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = BicycleManager()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'current_station']),
            models.Index(fields=['serial_number']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.model} ({self.serial_number})"
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name and serial number"""
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.serial_number}")
            self.slug = base_slug
        super().save(*args, **kwargs)
    
    @property
    def is_available(self):
        """Check if bicycle is available for rent"""
        return self.status == 'available'
    
    @property
    def needs_maintenance(self):
        """Check if bicycle needs maintenance"""
        from datetime import date
        if self.next_maintenance_date:
            return self.next_maintenance_date <= date.today()
        return False
    
    def mark_as_in_use(self):
        """Mark bicycle as in use"""
        self.status = 'in-use'
        self.save()
    
    def mark_as_available(self):
        """Mark bicycle as available"""
        self.status = 'available'
        self.save()
    
    def mark_as_reserved(self):
        """Mark bicycle as reserved"""
        self.status = 'reserved'
        self.save()
    
    def mark_as_maintenance(self):
        """Mark bicycle for maintenance"""
        self.status = 'maintenance'
        self.save()
    
    def increment_rental_count(self):
        """Increment total rental count"""
        self.total_rentals += 1
        self.save()
    
    def get_daily_rate(self):
        """Calculate daily rate (24 hours)"""
        return self.hourly_rate * 24


class MaintenanceLog(models.Model):
    """Track bicycle maintenance history"""
    
    bicycle = models.ForeignKey(
        Bicycle,
        on_delete=models.CASCADE,
        related_name='maintenance_logs'
    )
    description = models.TextField()
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    performed_by = models.CharField(max_length=200, blank=True)
    performed_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-performed_at']
    
    def __str__(self):
        return f"Maintenance for {self.bicycle.serial_number} on {self.performed_at.date()}"