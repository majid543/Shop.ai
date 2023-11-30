from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, login_view
from django.contrib.auth.views import LoginView


urlpatterns = [
    
    path('register/', register, name='register'),
    
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),  # Use Django's built-in LogoutView
    # Add other authentication-related views as needed
]