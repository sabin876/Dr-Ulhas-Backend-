from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(recipient_email: str, otp: str, token: str) -> None:
    """
    Send the OTP verification email to the patient.

    The verification link points to FRONTEND_BASE_URL (configured in settings)
    so the patient can open it and enter their OTP.  Fall back to the raw
    API endpoint when the setting is absent.
    """
    base_url = getattr(settings, "FRONTEND_BASE_URL", "http://localhost:8000/api")
    verification_link = f"{base_url}/verify-otp/?token={token}"

    subject = "Your Medical Report Access Code"

    message = (
        f"Hello,\n\n"
        f"A doctor has shared a medical report with you.\n\n"
        f"Your one-time verification code is:\n\n"
        f"    {otp}\n\n"
        f"This code expires in 10 minutes.\n\n"
        f"Alternatively, use the link below to verify directly:\n"
        f"{verification_link}\n\n"
        f"If you did not request this, please ignore this email.\n\n"
        f"— Medical Reports System"
    )

    html_message = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; max-width: 520px; margin: auto;">
        <h2 style="color: #2c7be5;">Medical Report Access</h2>
        <p>A doctor has shared a medical report with you.</p>
        <p>Your one-time verification code is:</p>
        <div style="font-size: 32px; font-weight: bold; letter-spacing: 8px;
                    background: #f4f7ff; border-radius: 6px; padding: 16px 24px;
                    display: inline-block; margin: 8px 0;">
          {otp}
        </div>
        <p style="color: #888; font-size: 13px;">This code expires in <strong>10 minutes</strong>.</p>
        <p>Or verify via link:</p>
        <a href="{verification_link}"
           style="background:#2c7be5;color:#fff;padding:10px 20px;
                  border-radius:4px;text-decoration:none;display:inline-block;">
          Verify &amp; View Report
        </a>
        <hr style="margin-top: 32px; border: none; border-top: 1px solid #eee;">
        <p style="font-size:12px;color:#aaa;">
          If you did not request this, please ignore this email.
        </p>
      </body>
    </html>
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        html_message=html_message,
        fail_silently=False,
    )