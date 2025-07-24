from rest_framework import permissions
from rest_framework.permissions import BasePermission, 
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated
    
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

