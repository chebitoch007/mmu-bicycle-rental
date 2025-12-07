from django.core.exceptions import ValidationError


def validate_file_size(file):
    """
    Validate uploaded file size (max 5MB)
    """
    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size cannot exceed {max_size_mb}MB')


def validate_university_id(value):
    """
    Validate MMU university ID format
    Expected format: STU/XXXXX or STF/XXXXX
    """
    if not value:
        return
    
    value = value.upper().strip()
    
    # Check format
    if not (value.startswith('STU/') or value.startswith('STF/')):
        raise ValidationError('University ID must start with STU/ (student) or STF/ (staff)')
    
    # Check length
    if len(value) < 8:
        raise ValidationError('Invalid university ID format')