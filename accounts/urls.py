from django.urls import path

from accounts.views import RegistrationView, UserProfileView,LoginView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('login/', LoginView.as_view(), name='login'),
]
