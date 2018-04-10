from django.urls import path, include
from .views import RegisterView, LoginView, IndexView


auth_paths = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('auth/', include((auth_paths, 'web'), namespace='auth')),
]
