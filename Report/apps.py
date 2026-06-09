# Report/apps.py
from django.apps import AppConfig


class ReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Report'
    verbose_name = "Medical Reports"

    def ready(self):
        # Signals removed - OTP now sent manually
        pass