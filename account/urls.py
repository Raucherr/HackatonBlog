from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='registration'),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    # path('logout/', views.LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile-update/<int:pk>/', ProfileUpdateView.as_view()),
    path('forgot_pass/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('change_password/', ChangePasswordView.as_view(), name="change-password"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]