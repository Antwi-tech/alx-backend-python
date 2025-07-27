# chats/middleware.py

from datetime import datetime
from django.http import HttpResponseForbidden
import logging
from datetime import datetime
from datetime import datetime, timedelta
from django.core.cache import cache
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Block access if not between 6 AM (06:00) and 9 PM (21:00)
        if not (6 <= current_hour < 21):
            return HttpResponseForbidden("❌ Chat is only accessible between 6AM and 9PM.")
        
        return self.get_response(request)

logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        return self.get_response(request)
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.time_window = timedelta(minutes=1)
        self.message_limit = 5

    def __call__(self, request):
        if request.method == 'POST' and '/messages/' in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            message_history = cache.get(ip, [])
            # Clean up timestamps older than the window
            message_history = [timestamp for timestamp in message_history if now - timestamp < self.time_window]

            if len(message_history) >= self.message_limit:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute.")

            # Record current message timestamp
            message_history.append(now)
            cache.set(ip, message_history, timeout=60)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get IP address from headers or fallback to REMOTE_ADDR"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip    


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: Restrict access to certain sensitive paths
        restricted_paths = ['/chats/delete/', '/chats/manage/']  # Adjust as needed
        user = request.user

        if any(path in request.path for path in restricted_paths):
            if not user.is_authenticated:
                return HttpResponseForbidden("Access denied: You must be logged in.")
            
            user_role = getattr(user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied: Insufficient permissions.")

        return self.get_response(request)    
    