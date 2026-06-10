import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from Report.services.email_async import send_email_async  # adjust path if needed

logger = logging.getLogger(__name__)


class EmailService:
    """
    Handles email operations (ASYNC using threads)
    """

    @staticmethod
    def send_otp_email(email, otp, token, report_id):
        """
        Send OTP email asynchronously (NON-BLOCKING)
        """

        try:
            base_url = getattr(
                settings,
                "FRONTEND_BASE_URL",
                "http://localhost:8000/api"
            )

            verification_link = f"{base_url}/verify-otp/?token={token}"

            subject = "Your Medical Report Access Code"

            message = f"""
            Hello,

            A doctor has shared a medical report with you.

            Your OTP is:
                {otp}

            This code expires in 10 minutes.

            Verify here:
            {verification_link}

            If you did not request this, ignore this email.
            """

            html_message = f"""
            <html>
              <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color:#2c7be5;">Medical Report Access</h2>

                <p>Your one-time verification code is:</p>

                <div style="
                    font-size:32px;
                    font-weight:bold;
                    letter-spacing:6px;
                    background:#f4f7ff;
                    padding:12px 20px;
                    display:inline-block;
                    border-radius:6px;">
                    {otp}
                </div>

                <p>This code expires in <b>10 minutes</b>.</p>

                <p>
                  <a href="{verification_link}"
                     style="background:#2c7be5;color:white;padding:10px 18px;
                            text-decoration:none;border-radius:4px;">
                     Verify & View Report
                  </a>
                </p>

                <hr>
                <small>If you did not request this, ignore this email.</small>
              </body>
            </html>
            """

            email_msg = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )

            email_msg.attach_alternative(html_message, "text/html")

            # ✅ ASYNC SEND (NON-BLOCKING)
            send_email_async(email_msg)

            logger.info(f"OTP email queued for {email}")
            return True

        except Exception as e:
            logger.error(f"Error preparing OTP email: {str(e)}")
            return False

    @staticmethod
    def send_report_notification(email, doctor_name, report_id):
        """
        Simple async report notification email
        """

        try:
            subject = "New Medical Report Available"

            message = f"""
            Hello,

            Dr. {doctor_name} has shared a new medical report with you.

            Report ID: {report_id}

            Please login to view it.
            """

            email_msg = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )

            send_email_async(email_msg)

            logger.info(f"Report notification queued for {email}")
            return True

        except Exception as e:
            logger.error(f"Error sending report notification: {str(e)}")
            return False