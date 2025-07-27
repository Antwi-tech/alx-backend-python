# chats/middleware.py

from datetime import datetime
from django.http import HttpResponseForbidden
import logging
from datetime import datetime
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