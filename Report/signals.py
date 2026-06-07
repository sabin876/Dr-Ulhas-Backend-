from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Report, ReportAccessOTP
from .services.otp_service import generate_otp, hash_otp
from .services.email_service import send_otp_email


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

    try:
        send_otp_email(
            recipient_email=instance.patient_email,
            otp=otp,
            token=str(otp_record.token),
        )
    except Exception:
        otp_record.delete()
        instance.delete()  # optional safety rollback