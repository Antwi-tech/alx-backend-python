from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to allow access only to the message sender/receiver or conversation participants.
    """

    def has_object_permission(self, request, view, obj):
        # For messages
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return obj.sender == request.user or obj.receiver == request.user
        
        # For conversations (assuming it has participants)
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        return False

permission_classes = [IsOwnerOrParticipant]
