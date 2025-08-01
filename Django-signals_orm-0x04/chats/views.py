from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render
from messaging.models import Message

@cache_page(60)  # Cache this view for 60 seconds
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender', 'receiver')
    return render(request, 'chats/conversation.html', {'messages': messages})
