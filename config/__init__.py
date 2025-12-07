"""
Settings package initialization
"""
import os

# Determine which settings to load
settings_module = os.environ.get(
    'DJANGO_SETTINGS_MODULE',
    'config.settings.development'
)

# Load correct settings
if 'development' in settings_module:
    from config.settings.development import *
elif 'production' in settings_module:
    from config.settings.production import *
else:
    from config.settings.base import *
