from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render
from messaging.models import Message


@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log them out first
    user.delete()    # Triggers post_delete signal
    return redirect('home')  # or any page after deletion


def get_replies_recursive(message):
    """Recursively fetch all replies to a message."""
    replies = message.replies.select_related('sender', 'receiver').all()
    thread = []
    for reply in replies:
        thread.append({
            "message": reply,
            "replies": get_replies_recursive(reply)
        })
    return thread


@login_required
def threaded_conversations(request):
    """View to display threaded messages for the logged-in user."""
    # Use select_related and prefetch_related
    root_messages = Message.objects.filter(
        sender=request.user
    ).filter(
        parent_message__isnull=True
    ).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        'replies__sender', 'replies__receiver'
    )

    conversations = []
    for msg in root_messages:
        conversations.append({
            "message": msg,
            "replies": get_replies_recursive(msg)
        })

    return render(request, 'messaging/threaded_conversations.html', {
        'conversations': conversations
    })
    
    
@cache_page(60)
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender', 'receiver')
    return render(request, 'messaging/conversation.html', {'messages': messages})
    