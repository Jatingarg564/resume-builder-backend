from django.urls import path
from .views import (
    SignupView,
    LoginView,
    ProfileView,
    ProfilePictureUploadView,
    PasswordResetView,
    PasswordResetConfirmView,
    UserSettingsView,
)

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile/picture/', ProfilePictureUploadView.as_view()),
    path('password/reset/', PasswordResetView.as_view()),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view()),
    path('settings/', UserSettingsView.as_view()),
]
