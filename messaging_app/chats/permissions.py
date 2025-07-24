from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Allows access only to message sender/receiver or conversation participants.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # For Message objects (assuming 'sender' and 'receiver' fields)
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return obj.sender == user or obj.receiver == user

        # For Conversation objects (assuming 'participants' is a many-to-many field)
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        return False

from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user
