from django.urls import path
from .views import SignupView
from .views import LoginView
from .views import ProfileView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
]
