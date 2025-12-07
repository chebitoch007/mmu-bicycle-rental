from django.db import models
from django.core.validators import MinValueValidator


class Station(models.Model):
    """
    Bicycle stations across MMU campus
    """
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="Short code (e.g., LIB, ENG)")
    description = models.TextField(blank=True)
    
    # Location
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        help_text="GPS Latitude"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        help_text="GPS Longitude"
    )
    
    # Capacity
    capacity = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1)],
        help_text="Maximum number of bicycles"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    operating_hours = models.CharField(
        max_length=100,
        default="24/7",
        help_text="e.g., '6:00 AM - 10:00 PM' or '24/7'"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def available_bikes_count(self):
        """Count of available bicycles at this station"""
        return self.bicycles.filter(status='available').count()
    
    @property
    def total_bikes_count(self):
        """Total bicycles at this station"""
        return self.bicycles.count()
    
    @property
    def occupancy_rate(self):
        """Calculate occupancy percentage"""
        if self.capacity == 0:
            return 0
        return (self.total_bikes_count / self.capacity) * 100
    
    @property
    def has_capacity(self):
        """Check if station can accept more bikes"""
        return self.total_bikes_count < self.capacity
    
    def get_location_url(self):
        """Get Google Maps URL if coordinates available"""
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return None