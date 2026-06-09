import hashlib
import secrets
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class OTPService:
    """
    Service to handle OTP generation and verification
    """
    
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    
    @staticmethod
    def generate_otp():
        """
        Generate a 6-digit OTP using secrets (cryptographically secure)
        
        Returns:
            str: 6-digit OTP
        """
        return ''.join(secrets.choice('0123456789') for _ in range(OTPService.OTP_LENGTH))
    
    @staticmethod
    def hash_otp(otp):
        """
        Hash OTP using SHA-256
        
        Args:
            otp: Plain OTP string
            
        Returns:
            str: SHA-256 hex digest
        """
        return hashlib.sha256(otp.encode()).hexdigest()
    
    @staticmethod
    def verify_otp(plain_otp, otp_hash):
        """
        Verify OTP by comparing hashes
        
        Args:
            plain_otp: Plain OTP from user
            otp_hash: Stored OTP hash
            
        Returns:
            bool: True if OTP matches
        """
        return OTPService.hash_otp(plain_otp) == otp_hash
    
    @staticmethod
    def create_otp_record(report, email):
        """
        Create and save OTP record
        
        Args:
            report: Report instance
            email: Patient email
            
        Returns:
            tuple: (ReportAccessOTP instance, plain OTP string)
        """
        from Report.models import ReportAccessOTP
        
        otp = OTPService.generate_otp()
        otp_hash = OTPService.hash_otp(otp)
        
        otp_record = ReportAccessOTP.objects.create(
            report=report,
            email=email,
            otp_hash=otp_hash,
        )
        
        logger.info(f"OTP record created for {email}, report {report.id}")
        return otp_record, otp
    
    @staticmethod
    def validate_and_mark_used(otp_record, plain_otp):
        """
        Validate OTP and mark as used
        
        Args:
            otp_record: ReportAccessOTP instance
            plain_otp: Plain OTP from user
            
        Returns:
            tuple: (is_valid: bool, error_message: str or None)
        """
        # Check if already used
        if otp_record.is_used:
            return False, "OTP has already been used"
        
        # Check expiry
        if otp_record.is_expired:
            return False, "OTP has expired"
        
        # Verify OTP
        if not OTPService.verify_otp(plain_otp, otp_record.otp_hash):
            return False, "Invalid OTP"
        
        # Mark as verified and used
        otp_record.is_verified = True
        otp_record.is_used = True
        otp_record.save()
        
        logger.info(f"OTP verified and marked used for {otp_record.email}")
        return True, None