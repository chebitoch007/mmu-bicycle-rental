from datetime import datetime, timedelta
from django.utils import timezone


def format_duration(duration):
    """
    Format timedelta into readable string
    Example: "2 hours 30 minutes"
    """
    if not duration:
        return "0 minutes"
    
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    
    return " ".join(parts) if parts else "less than a minute"


def calculate_rental_cost(hourly_rate, duration_hours, late_hours=0):
    """
    Calculate rental cost including late fees
    """
    base_cost = hourly_rate * duration_hours
    late_fee = 0
    
    if late_hours > 0:
        late_fee = hourly_rate * late_hours * 0.5  # 50% extra for late hours
    
    return base_cost + late_fee


def get_time_remaining_display(expires_at):
    """
    Get human-readable time remaining
    """
    if not expires_at:
        return "Unknown"
    
    now = timezone.now()
    if expires_at <= now:
        return "Expired"
    
    remaining = expires_at - now
    return format_duration(remaining)


def is_during_operating_hours(operating_hours):
    """
    Check if current time is within operating hours
    """
    if operating_hours == "24/7":
        return True
    
    # Parse operating hours (e.g., "6:00 AM - 10:00 PM")
    # This is a simplified version
    return True  # Always return True for now