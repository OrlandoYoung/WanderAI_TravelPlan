from django.urls import path
from .views import SendEmailCodeView,RegisterView, LoginView, LogoutView, UserProfileView

urlpatterns = [
    path('send_email_code', SendEmailCodeView.as_view()),
    path('register', RegisterView.as_view(), name='user_register'),
    path('login', LoginView.as_view(), name='user_login'),
    path('logout', LogoutView.as_view(), name='user_logout'),
    path('profile', UserProfileView.as_view(), name='user_profile'),
]