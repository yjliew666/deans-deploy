import logging
from django.contrib import admin
from .models import (
    Operator,
    Crisis,
    CrisisType,
    CrisisAssistance,
    SiteSettings,
    EmergencyAgencies,
    SocialMediaAccount
)

# Initialize Logger
logger = logging.getLogger(__name__)

class CrisisAdmin(admin.ModelAdmin):
    """
    Custom Admin View for Crisis model.
    Enables visibility toggling directly from the list view.
    """
    list_display = ('crisis_id', 'crisis_description', 'crisis_time', 'visible')
    list_editable = ('visible',)

# Register Crisis with its custom admin class
try:
    admin.site.register(Crisis, CrisisAdmin)
    logger.info("Registered Crisis model with custom CrisisAdmin.")
except Exception as e:
    logger.error(f"Failed to register Crisis admin: {e}")

# Register standard models in bulk to reduce repetition
models_to_register = [
    Operator,
    CrisisType,
    CrisisAssistance,
    SiteSettings,
    EmergencyAgencies,
    SocialMediaAccount
]

# Register remaining models
try:
    admin.site.register(models_to_register)
    logger.info(f"Registered models: {[m.__name__ for m in models_to_register]}")
except Exception as e:
    logger.error(f"Failed to register standard models: {e}")