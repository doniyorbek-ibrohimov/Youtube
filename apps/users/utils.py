import random
from django.core.cache import cache

MAX_ATTEMPTS = 5
OPT_TTL = 600  # 10 minutes
ATTEMPT_TTL = OPT_TTL  # 10 minutes

def generate_otp():
    return str(random.randint(100000, 999999))

def store_otp(email, otp, expiry=600):
    # storing OTP in Redis with an expiry time (10 minutes)
    cache.set(f"otp_{email}", otp, timeout=expiry)
    cache.delete(f"otp_attempts_{email}")  # reset attempts on new OTP

def increment_attempts(email):
    attempts = cache.get(f"otp_attempts_{email}", 0)
    attempts += 1
    cache.set(f"otp_attempts_{email}", attempts, timeout=ATTEMPT_TTL)
    return attempts

def attempts_exceeded(email: str) -> bool:
    attempts = cache.get(f"otp_attempts_{email}", 0)
    return attempts >= MAX_ATTEMPTS

def reset_attempts(email):
    cache.delete(f"otp_attempts_{email}")


def verify_otp(email: str, otp: str) -> tuple[bool, str | None]:
    if attempts_exceeded(email):
        return False, "too many attempts. Please request a new OTP."

    stored_otp = cache.get(f"otp_{email}")
    if stored_otp is None:
        return False, "OTP has expired or does not exist. Please request a new OTP."

    if stored_otp != otp:
        increment_attempts(email)
        return False, "Invalid OTP. Please try again."

    # OTP is valid
    cache.delete(f"otp_{email}")  # remove OTP after successful verification
    reset_attempts(email)  # reset attempts on successful verification
    return True, None

