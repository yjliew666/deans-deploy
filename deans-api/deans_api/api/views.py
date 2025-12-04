import logging
from typing import List

from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, generics, status
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    BasePermission
)
from rest_framework.response import Response

from .models import (
    Crisis,
    CrisisAssistance,
    CrisisType,
    SiteSettings,
    EmergencyAgencies
)
from .permissions import NotAllowed
from .serializer import (
    CrisisSerializer,
    CrisisAssistanceSerializer,
    CrisisTypeSerializer,
    UserSerializer,
    UserAdminSerializer,
    SiteSettingsSerializer,
    EmergencyAgenciesSerializer
    # Note: EmergencyAgenciesUpdateSerializer was removed in previous refactor
    # as it was identical to the base serializer.
)

# Initialize Logger
logger = logging.getLogger(__name__)


class PublicCreateReadAdminModifyMixin:
    """
    DRY Mixin: Defaults to AllowAny for list/create/retrieve.
    Requires Admin privileges for Update/Delete.
    """
    def get_permissions(self) -> List[BasePermission]:
        if self.action in ['list', 'retrieve', 'create']:
            return [AllowAny()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        """Log creation events."""
        instance = serializer.save()
        logger.info(f"Created {self.queryset.model.__name__} ID {instance.pk}")

    def perform_update(self, serializer):
        """Log update events."""
        instance = serializer.save()
        logger.info(f"Updated {self.queryset.model.__name__} ID {instance.pk}")

class CrisisViewSet(PublicCreateReadAdminModifyMixin, viewsets.ModelViewSet):
    """
    Return a list of all existing crises.
    """
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer


class CrisisUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    """
    Crisis update API. Requires full field submission (PUT).
    """
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer
    permission_classes = [IsAdminUser]  # Explicitly defining permission for safety

    def put(self, request, *args, **kwargs):
        logger.info(f"Full update requested for Crisis ID {kwargs.get('pk')}")
        return self.update(request, *args, **kwargs)


class CrisisPartialUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    """
    Crisis partial update API. Allows modifying specific fields (PATCH).
    """
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        # Note: Usually PATCH is mapped to partial_update, but keeping 'put'
        # per original code requirement, though calling partial_update inside.
        logger.info(f"Partial update requested for Crisis ID {kwargs.get('pk')}")
        return self.partial_update(request, *args, **kwargs)


# ==========================================
# Helper Views (Assistance, Type, Settings)
# ==========================================

class CrisisAssistanceViewSet(PublicCreateReadAdminModifyMixin, viewsets.ModelViewSet):
    queryset = CrisisAssistance.objects.all()
    serializer_class = CrisisAssistanceSerializer


class CrisisTypeViewSet(PublicCreateReadAdminModifyMixin, viewsets.ModelViewSet):
    queryset = CrisisType.objects.all()
    serializer_class = CrisisTypeSerializer


class SiteSettingViewSet(PublicCreateReadAdminModifyMixin, viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and creating user instances.
    Restricted: Only Admins can list or create. Updating via this endpoint is disabled.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self) -> List[BasePermission]:
        if self.action in ['list', 'create']:
            return [IsAdminUser()]
        # Default to NotAllowed for other actions to prevent accidental deletion via this endpoint
        return [NotAllowed()]

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f"Admin created new user: {user.username}")


class UserPartialUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    """
    Specific endpoint for Admin to partially update a user.
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        logger.info(f"Admin updating user ID {kwargs.get('pk')}")
        return self.partial_update(request, *args, **kwargs)

class EmergencyAgenciesView(PublicCreateReadAdminModifyMixin, viewsets.ModelViewSet):
    queryset = EmergencyAgencies.objects.all()
    serializer_class = EmergencyAgenciesSerializer


class EmergencyAgenciesPartialUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = EmergencyAgencies.objects.all()
    serializer_class = EmergencyAgenciesSerializer
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        logger.info(f"Updating Emergency Agency ID {kwargs.get('pk')}")
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Custom delete handler.
        """
        try:
            instance = self.get_object()
            agency_name = instance.agency
            instance.delete()
            logger.info(f"Deleted Emergency Agency: {agency_name}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting agency: {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)