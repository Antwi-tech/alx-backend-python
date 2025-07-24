from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Allows access only to message sender/receiver or conversation participants.
    """

    def has_object_permission(self, request, view, obj):
        """
        - GET, POST, PUT, PATCH, DELETE are allowed
          only if the user is a participant of the conversation.
        """
        user = request.user
        conversation = getattr(obj, 'conversation', None)

        # Explicit check for unsafe methods
        if request.method in ["PUT", "PATCH", "DELETE", "POST", "GET"]:
            if conversation:
                return user in conversation.participants.all()

        # Default deny
        return False
