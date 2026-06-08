from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Report, ReportAccessOTP

@admin.register(Report)
class ReportAdmin(ModelAdmin):
    list_display = ('id', 'patient_email', 'doctor', 'created_at')
    search_fields = ('patient_email', 'content')
    list_filter = ('created_at',)

@admin.register(ReportAccessOTP)
class ReportAccessOTPAdmin(ModelAdmin):
    list_display = ('email', 'report', 'is_verified', 'is_used', 'created_at', 'expires_at')
    search_fields = ('email',)
    list_filter = ('is_verified', 'is_used', 'created_at')
