from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="registration"),
    path('activate/', ActivationView.as_view(), name="activation"),
    path('login/', LoginView.as_view(), name="signin"),
    path('logout/', LogoutView.as_view(), name="signout"),
    path('forgot_pass/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('change_password/', ChangePasswordView.as_view(), name="change-password")
]