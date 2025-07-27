# chats/middleware.py

import logging
from datetime import datetime

# Set up logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')  # Log file in project root
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Middleware class
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(message)
        return self.get_response(request)
