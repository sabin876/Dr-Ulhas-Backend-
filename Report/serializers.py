import uuid
from rest_framework import serializers
from .models import Report, ReportAccessOTP
from .services.otp_service import OTPService


class CreateReportSerializer(serializers.ModelSerializer):
    """
    Used by the doctor to create a new report.
    `doctor` is injected from request.user in the view — not accepted from the client.
    """
    class Meta:
        model = Report
        fields = ["patient_email", "content", "report_file"]


class SendOTPSerializer(serializers.Serializer):
    """
    Send OTP using email address
    """
    report_id = serializers.IntegerField(required=False)
    email = serializers.EmailField()

    def validate(self, data):
        report_id = data.get("report_id")
        email = data.get("email")

        if report_id:
            try:
                report = Report.objects.get(pk=report_id)
            except Report.DoesNotExist:
                raise serializers.ValidationError(
                    {"report_id": "Report not found."}
                )

            if report.patient_email.lower() != email.lower():
                raise serializers.ValidationError(
                    {"email": "This email does not match the report's patient email."}
                )
        else:
            report = Report.objects.filter(patient_email__iexact=email).order_by("-created_at").first()
            if not report:
                raise serializers.ValidationError(
                    {"email": "No report found for this email address."}
                )

        data["report"] = report
        return data

class VerifyOTPSerializer(serializers.Serializer):
    """
    Verify OTP using email + OTP code
    """
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6)
    email = serializers.EmailField()

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only digits")
        return value

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        # Step 1: get latest OTP record for email
        otp_record = ReportAccessOTP.objects.select_related("report").filter(
            email=email
        ).order_by('-created_at').first()

        if not otp_record:
            raise serializers.ValidationError({
                "email": "No OTP request found for this email."
            })

        # Step 2: check expiry
        if otp_record.is_expired:
            raise serializers.ValidationError({
                "otp": "OTP has expired. Please request a new one."
            })

        # Step 3: check reuse
        if otp_record.is_used:
            raise serializers.ValidationError({
                "otp": "This OTP has already been used."
            })

        # Step 4: verify OTP hash
        if not OTPService.verify_otp(otp, otp_record.otp_hash):
            raise serializers.ValidationError({
                "otp": "Invalid OTP."
            })

        # Step 5: attach objects
        data["otp_record"] = otp_record
        data["report"] = otp_record.report

        return data
class ReportSerializer(serializers.ModelSerializer):
    """
    Serializer for accessing verified reports
    """
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    
    class Meta:
        model = Report
        fields = ['id', 'doctor_name', 'patient_email', 'content', 'report_file', 'created_at']
        read_only_fields = fields