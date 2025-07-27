from rest_framework import generics, permissions, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwnerOrParticipant, IsParticipantOfConversation
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MessagePagination
import django_filters
from django.db.models import Q
from .models import Message

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user) | Message.objects.filter(receiver=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageDetailView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrParticipant]

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                raise PermissionDenied("Conversation does not exist.")

            if self.request.user not in conversation.participants.all():
                raise PermissionDenied("You are not a participant in this conversation.")

            return Message.objects.filter(conversation=conversation)
        else:
            # fallback in case it's not a nested route
            return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only messages from conversations the user is in
        return Message.objects.filter(conversation__participants=self.request.user)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            sender=self.request.user
        ) | Message.objects.filter(
            recipient=self.request.user
        )    
        
class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name="sender__username", lookup_expr='iexact')
    recipient = django_filters.CharFilter(field_name="recipient__username", lookup_expr='iexact')
    start_date = django_filters.IsoDateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.IsoDateTimeFilter(field_name="timestamp", lookup_expr='lte')
    user = django_filters.CharFilter(method='filter_user')
        
 
class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        return Message.objects.filter(
            sender=self.request.user
        ) | Message.objects.filter(
            recipient=self.request.user
        )       