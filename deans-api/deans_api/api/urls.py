import logging
from django.urls import include, path
from rest_framework import routers

from .views import (
    CrisisViewSet,
    CrisisAssistanceViewSet,
    CrisisTypeViewSet,
    CrisisUpdateView,
    CrisisPartialUpdateView,
    UserViewSet,
    UserPartialUpdateView,
    EmergencyAgenciesView,
    EmergencyAgenciesPartialUpdateView,
    SiteSettingViewSet
)

# Initialize Logger
logger = logging.getLogger(__name__)

"""
The Router automatically generates the following API structure:
    - /crises/
    - /crisisassistance/
    - /crisistype/
    - /users/
    - /emergencyagencies/
    - /sitesettings/
"""
router = routers.DefaultRouter()
router.register('crises', CrisisViewSet)
router.register('crisisassistance', CrisisAssistanceViewSet)
router.register('crisistype', CrisisTypeViewSet)
router.register('users', UserViewSet)
router.register('emergencyagencies', EmergencyAgenciesView)
router.register('sitesettings', SiteSettingViewSet)

logger.info("API Router configured successfully.")

urlpatterns = [
    # Built-in Authentication & Registration
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),

    # Router Generated URLs
    # We include these first to handle the bulk of standard CRUD operations
    path('', include(router.urls)),

    # Specific overrides or specialized update paths
    path(
        'crises/update/<int:pk>/', 
        CrisisUpdateView.as_view(), 
        name='crisis_update'
    ),
    path(
        'crises/update-partial/<int:pk>/', 
        CrisisPartialUpdateView.as_view(), 
        name='crisis_partial_update'
    ),
    path(
        'users/update-partial/<int:pk>/', 
        UserPartialUpdateView.as_view(), 
        name='user_partial_update'
    ),
    path(
        'emergencyagencies/update-partial/<int:pk>/', 
        EmergencyAgenciesPartialUpdateView.as_view(), 
        name='emergencyagency_partial_update'
    ),
]