import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Report(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports",
    )
    patient_email = models.EmailField()
    content = models.TextField()
    report_file = models.FileField(upload_to="reports/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report #{self.id} — {self.patient_email}"


class ReportAccessOTP(models.Model):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name="otps",
    )
    email = models.EmailField()
    otp_hash = models.CharField(max_length=64)          # SHA-256 hex digest
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_verified = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.email} — report #{self.report_id}"