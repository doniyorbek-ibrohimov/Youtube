from django.urls import path
from .views import (
    RegisterView,
    VerifyOTPView,
    UserDetailView,
    ChangePasswordView,
)

urlpatterns = [
    # Public registration endpoint
    path("register/", RegisterView.as_view(), name="user-register"),

    # Verify OTP for email confirmation
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),

    # Get current authenticated user's profile
    path("me/", UserDetailView.as_view(), name="user-me"),

    # Change password
    path("password/change/", ChangePasswordView.as_view(), name="change-password"),
]
