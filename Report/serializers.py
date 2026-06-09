import uuid
from rest_framework import serializers
from .models import Report


class CreateReportSerializer(serializers.ModelSerializer):
    """
    Used by the doctor to create a new report.
    `doctor` is injected from request.user in the view — not accepted from the client.
    """

    class Meta:
        model = Report
        fields = ["patient_email", "content"]


class SendOTPSerializer(serializers.Serializer):
    report_id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)
    token = serializers.UUIDField(required=False)

    def validate(self, data):
        token = data.get("token")
        if token:
            try:
                from .models import ReportAccessOTP
                otp_record = ReportAccessOTP.objects.select_related("report").get(token=token)
                data["report"] = otp_record.report
                data["email"] = otp_record.email
                data["otp_record"] = otp_record
            except ReportAccessOTP.DoesNotExist:
                raise serializers.ValidationError(
                    {"token": "Invalid or expired token."}
                )
            return data

        report_id = data.get("report_id")
        email = data.get("email")
        if not report_id or not email:
            raise serializers.ValidationError(
                "Either token or (report_id and email) must be provided."
            )

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

        data["report"] = report
        return data


class VerifyOTPSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    otp = serializers.CharField(min_length=6, max_length=6)
    email = serializers.EmailField()


class ReportSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()

    class Meta:
        model = Report
        fields = ["id", "doctor", "patient_email", "content", "created_at"]