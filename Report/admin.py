from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import signals
from django import forms
from ckeditor.widgets import CKEditorWidget
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Report, ReportAccessOTP


class ReportAdminForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = "__all__"
        widgets = {
            "content": CKEditorWidget(),
        }


# @admin.register(Report)
class ReportAdmin(ModelAdmin):
    form = ReportAdminForm
    list_display = ('id', 'doctor', 'patient_email', 'created_at', 'send_otp_button')
    list_filter = ('doctor', 'created_at')
    search_fields = ('patient_email', 'content')
    readonly_fields = ('created_at', 'doctor')
    
    fieldsets = (
        ('Doctor Information', {
            'fields': ('doctor',)
        }),
        ('Patient Information', {
            'fields': ('patient_email',)
        }),
        ('Report Details', {
            'fields': ('content', 'report_file')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    class Media:
        js = (
            'Report/js/report_templates.js',
        )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('patient_email',)
        return self.readonly_fields
    
    @display(description="Actions")
    def send_otp_button(self, obj):
        """Display Send OTP button in list view"""
        if obj.id:
            url = reverse('admin:report_send_otp', args=[obj.id])
            return format_html(
                '<a class="bg-primary-600 hover:bg-primary-700 text-white font-medium py-1 px-3 rounded text-xs inline-block" href="{}">Send OTP</a>',
                url
            )
        return "-"
    
    def save_model(self, request, obj, form, change):
        """Set doctor to current user when creating report"""
        if not change:  # Creating new object
            obj.doctor = request.user
        super().save_model(request, obj, form, change)
    
    def get_urls(self):
        """Add custom URL for sending OTP"""
        from django.urls import path
        from .views import SendOTPAdminView
        
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:report_id>/send-otp/',
                self.admin_site.admin_view(SendOTPAdminView.as_view()),
                name='report_send_otp',
            ),
        ]
        return custom_urls + urls


# @admin.register(ReportAccessOTP)
class ReportAccessOTPAdmin(ModelAdmin):
    list_display = ('id', 'report', 'email', 'is_verified', 'is_used', 'is_expired', 'created_at')
    list_filter = ('is_verified', 'is_used', 'created_at')
    search_fields = ('email', 'report__patient_email')
    readonly_fields = ('token', 'otp_hash', 'created_at', 'expires_at', 'is_expired_display')
    
    fieldsets = (
        ('OTP Record', {
            'fields': ('report', 'email', 'token')
        }),
        ('OTP Hash', {
            'fields': ('otp_hash',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_verified', 'is_used', 'is_expired_display')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_expired_display(self, obj):
        """Display expiry status with color"""
        if obj.is_expired:
            return format_html('<span style="color: red;">✗ Expired</span>')
        return format_html('<span style="color: green;">✓ Active</span>')
    is_expired_display.short_description = "Expiry Status"
    
    def has_add_permission(self, request):
        """Prevent manual creation via admin"""
        return False
