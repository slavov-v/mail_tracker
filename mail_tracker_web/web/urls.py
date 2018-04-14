from django.urls import path, include
from .views import (
    RegisterView,
    LoginView,
    IndexView,
    MessageDetailView,
    DeleteMessageView,
    SendEmailView
)


auth_paths = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('messages/<int:message_id>/', MessageDetailView.as_view(), name='message_detail'),
    path('delete/<int:message_id>/', DeleteMessageView.as_view(), name='delete_message'),
    path('send-email/', SendEmailView.as_view(), name='send_email'),
    path('auth/', include((auth_paths, 'web'), namespace='auth')),
]
