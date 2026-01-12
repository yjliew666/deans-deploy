import logging
from rest_framework import permissions

# Get the logger instance
logger = logging.getLogger(__name__)

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow owners of an object to edit it.
    Read permissions are allowed to any request.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the object.
        # We assume the model instance has an 'author' attribute.
        is_author = (obj.author == request.user)

        if not is_author:
            logger.warning(
                f"Write permission denied. User '{request.user}' tried to modify "
                f"object '{obj}' owned by '{obj.author}'."
            )

        return is_author


class NotAllowed(permissions.BasePermission):
    """
    Global permission to block access to a view.
    """
    message = 'No access'

    def has_permission(self, request, view):
        logger.warning(
            f"Access blocked by NotAllowed permission. "
            f"User: '{request.user}', Path: '{request.path}'"
        )
        return False