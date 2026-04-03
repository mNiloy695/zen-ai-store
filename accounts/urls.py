from django.urls import path

from accounts.views import RegistrationView, UserProfileView,LoginView,LogoutView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
