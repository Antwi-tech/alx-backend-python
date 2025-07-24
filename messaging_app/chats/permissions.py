from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


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


class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to only allow participants of a conversation
        to interact with its messages or conversations.
        """
        conversation = getattr(obj, 'conversation', None)

        if conversation:
            return request.user in conversation.participants.all()

        # If we're working directly with a conversation
        return request.user in obj.participants.all()