from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render
from messaging.models import Message

@cache_page(60)
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender', 'receiver')
    return render(request, 'messaging/conversation.html', {'messages': messages})
