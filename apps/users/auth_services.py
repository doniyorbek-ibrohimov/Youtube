from django.contrib.auth import get_user_model
from apps.users.utils import generate_otp, store_otp, verify_otp
from apps.users.tasks import send_otp_email

User = get_user_model()

class EmailVeritificationService:

    @staticmethod
    def send_otp(user: User) -> None: # type: ignore
        """
        Generates and sends an OTP to the user's email for verification.
        """
        otp = generate_otp()
        store_otp(user.email, otp)
        send_otp_email.delay(user.email, otp) # type: ignore

    @staticmethod
    def verify_otp(user: User, otp: str) -> tuple[bool, str | None]: # type: ignore
        """
        Verifies OTP and activates user
        """
        success, error = verify_otp(user.email, otp) # type: ignore
        if not success:
            return False, error
        
        user.is_active = True
        user.is_email_verified = True
        user.save(update_fields=['is_active', 'is_email_verified'])
        return True, None
    


def change_user_password(*, user, new_password)
    """
    Changes the user's password
    """
    user.set_password(new_password)
    user.save(update_fields=['password'])

