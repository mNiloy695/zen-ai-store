from django.urls import path

from accounts.views import RegistrationView, UserProfileView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
