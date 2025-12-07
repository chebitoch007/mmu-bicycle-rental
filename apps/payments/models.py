from django.db import models
from django.core.validators import MinValueValidator
from apps.accounts.models import User
from apps.rentals.models import Rental


class Payment(models.Model):
    """
    Payment tracking for rentals
    Supports multiple payment methods
    """
    
    METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='payments')
    
    # Payment details
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Transaction details
    transaction_id = models.CharField(max_length=200, unique=True, blank=True, null=True)
    reference_number = models.CharField(max_length=200, blank=True)
    
    # Provider response
    provider_response = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['rental', 'status']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        return f"Payment #{self.id} - {self.user.username} - {self.amount} KES"
    
    @property
    def is_completed(self):
        """Check if payment is completed"""
        return self.status == 'completed'
    
    @property
    def is_pending(self):
        """Check if payment is pending"""
        return self.status in ['pending', 'processing']
    
    def mark_as_completed(self, transaction_id=None):
        """Mark payment as completed"""
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        if transaction_id:
            self.transaction_id = transaction_id
        self.save()
    
    def mark_as_failed(self):
        """Mark payment as failed"""
        self.status = 'failed'
        self.save()


class Refund(models.Model):
    """
    Refund tracking
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"Refund for Payment #{self.payment.id} - {self.amount} KES"