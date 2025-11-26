from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow author to modify and everyone to read
    """
    def has_object_permission(self, request, view, obj):
        # Every user is allowed to read, safe HTTP will bypass directly
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only author can write permission
        return obj.author == request.user

class NotAllowed(permissions.BasePermission):
    """
    Not allow anyony to access
    """
    message = 'No access'
    def has_permission(self, request, view):
        return False