from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.users.api.serializers import (
    RegisterSerializer, UserSerializer, PasswordChangeSerializer
)
from apps.users.auth_services import EmailVeritificationService, change_user_password
from apps.users.auth_selectors import get_user_me


class RegisterView(APIView):
    # POST /api/users/register/
    # Registers a new user and sends OTP for email verification
    permission_classes = []  # Allow anyone to register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save new user
        user = serializer.save()

        # Send OTP to email
        success, error = EmailVeritificationService.send_otp(user)  # type: ignore
        if not success:
            return Response(
                {"error": error},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        return Response(
            {
                "message": (
                    "User registered successfully. "
                    "Please check your email for the OTP to verify your account."
                )
            },
            status=status.HTTP_201_CREATED
        )


class VerifyOTPView(APIView):
    # POST /api/users/verify-otp/
    # Verifies user's email using OTP
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        otp = request.data.get("otp")

        # Verify OTP and activate user
        success, error = EmailVeritificationService.verify_otp(user, otp)
        if not success:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Email verified successfully."},
            status=status.HTTP_200_OK
        )


class UserDetailView(APIView):
    # GET /api/users/me/
    # Returns current authenticated user's profile
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_user_me(user=request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    # POST /api/users/password/change/
    # Allows authenticated users to change their password
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # Call service to update password
        change_user_password(
            user=request.user,
            new_password=serializer.validated_data["new_password"]  # type: ignore
        )

        return Response(
            {"detail": "Password changed successfully."},
            status=status.HTTP_200_OK
        )
