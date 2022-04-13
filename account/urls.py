# from django.urls import path
# from .views import *
# from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
#
# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='registration'),
#     path('activate/<str:activation_code>/', ActivationView.as_view()),
#     path('login/', LoginView.as_view()),
#     # path('logout/', views.LogoutView.as_view()),
#     path('profile/', ProfileView.as_view()),
#     path('profile-update/<int:pk>/', ProfileUpdateView.as_view()),
#     path('forgot_pass/', ForgotPasswordView.as_view(), name="forgot-password"),
#     path('change_password/', ChangePasswordView.as_view(), name="change-password"),
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
# ]


from django.urls import path, include

from . import views
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('reg/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', views.ActivationView.as_view()),
    path('log/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    # path('profile-create/', ProfileCreateView.as_view()),
    path('profile-update/<int:pk>/', views.ProfileUpdateView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]