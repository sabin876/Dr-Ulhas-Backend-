from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_otp_email_task(self, email, otp, token, report_id):
    """
    Celery task to send OTP email asynchronously
    
    Args:
        email: Patient's email address
        otp: Plain OTP (6-digit code)
        token: UUID token for verification
        report_id: Report ID for reference
    """
    try:
        subject = "Your Medical Report Access OTP"
        
        # Create verification link
        verification_link = f"{settings.FRONTEND_URL}/verify-otp?token={token}"
        
        # Context for email template
        context = {
            "otp": otp,
            "verification_link": verification_link,
            "token": str(token),
            "otp_expiry": "10 minutes",
            "report_id": report_id,
        }
        
        # Render HTML email
        html_message = render_to_string("emails/otp_email.html", context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email="contact@drulhasorthopedic.com",
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"OTP email sent successfully to {email}")
        return f"OTP email sent successfully to {email}"
    
    except Exception as exc:
        print(f"Error sending OTP email to {email}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_report_notification_email(self, email, doctor_name, report_id):
    """
    Task to send report notification email to patient
    """
    try:
        subject = f"New Medical Report from Dr. {doctor_name}"
        
        context = {
            "doctor_name": doctor_name,
            "report_id": report_id,
        }
        
        html_message = render_to_string("emails/report_notification.html", context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )   
        
        logger.info(f"Report notification sent to {email}")
        return f"Report notification sent to {email}"
    
    except Exception as exc:
        logger.error(f"Failed to send report notification to {email}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)