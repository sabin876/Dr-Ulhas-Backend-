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
    report_id = serializers.IntegerField()
    email = serializers.EmailField()

    def validate(self, data):
        try:
            report = Report.objects.get(pk=data["report_id"])
        except Report.DoesNotExist:
            raise serializers.ValidationError(
                {"report_id": "Report not found."}
            )

        if report.patient_email.lower() != data["email"].lower():
            raise serializers.ValidationError(
                {"email": "This email does not match the report's patient email."}
            )

        data["report"] = report
        return data


class VerifyOTPSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    otp = serializers.CharField(min_length=6, max_length=6)


class ReportSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()

    class Meta:
        model = Report
        fields = ["id", "doctor", "patient_email", "content", "created_at"]