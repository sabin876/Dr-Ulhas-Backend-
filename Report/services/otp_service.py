import hashlib
import random
import string


def generate_otp(length: int = 6) -> str:
    """Return a cryptographically-adequate numeric OTP string."""
    return "".join(random.choices(string.digits, k=length))


def hash_otp(otp: str) -> str:
    """Return the SHA-256 hex digest of *otp*."""
    return hashlib.sha256(otp.encode()).hexdigest()


def verify_otp(plain_otp: str, stored_hash: str) -> bool:
    """Return True when the hash of *plain_otp* matches *stored_hash*."""
    return hash_otp(plain_otp) == stored_hash