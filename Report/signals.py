from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Report, ReportAccessOTP
from .services.otp_service import generate_otp, hash_otp
from .sender import send_otp_email_task


@receiver(post_save, sender=Report)
def send_report_otp(sender, instance, created, **kwargs):
    if not created:
        return

    otp = generate_otp()

    otp_record = ReportAccessOTP.objects.create(
        report=instance,
        email=instance.patient_email,
        otp_hash=hash_otp(otp),
    )
    print(f"Generated OTP {otp} for report {instance.id} and email {instance.patient_email}")
    print(f"OTP record created with token {otp_record.token} and expires at {otp_record.expires_at}")
    print(instance.patient_email)
    try:
        send_otp_email_task(
            recipient_email=instance.patient_email,
            otp=otp,
            token=str(otp_record.token),
        )
    except Exception:
        otp_record.delete()
        instance.delete()  # optional safety rollback