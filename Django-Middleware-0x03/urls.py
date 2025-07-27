from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .chats.views import MessageListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('messaging_app.chats.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('messages/', MessageListView.as_view(), name='message-list'),
    
]
