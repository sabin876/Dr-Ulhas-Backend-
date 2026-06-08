from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Report, ReportAccessOTP
from .serializers import (
    CreateReportSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
    ReportSerializer,
)
from .services.otp_service import generate_otp, hash_otp, verify_otp
from .services.email_service import send_otp_email


class CreateReportView(APIView):
    """
    POST /api/reports/create/

    Doctor-only endpoint (must be authenticated).
    Creates a Report and immediately generates + emails an OTP to the patient.

    Body: { "patient_email": "patient@example.com", "content": "..." }

    Response 201:
    {
        "report": { id, doctor, patient_email, content, created_at },
        "token":  "<uuid>",
        "detail": "Report created and OTP sent to patient."
    }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Bind the authenticated doctor to the report
        report = serializer.save(doctor=request.user)

        # Generate OTP and persist hashed version
        otp = generate_otp()
        otp_record = ReportAccessOTP.objects.create(
            report=report,
            email=report.patient_email,
            otp_hash=hash_otp(otp),
        )

        # Send email — roll back both records on failure so nothing is left dangling
        try:
            send_otp_email(
                recipient_email=report.patient_email,
                otp=otp,
                token=str(otp_record.token),
            )
        except Exception:
            otp_record.delete()
            report.delete()
            return Response(
                {"detail": "Report created but OTP email failed. Please try again."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {
                "detail": "Report created and OTP sent to patient.",
                "report": ReportSerializer(report).data,
                "token": str(otp_record.token),
            },
            status=status.HTTP_201_CREATED,
        )

class SendOTPView(APIView):
    """
    POST /api/send-otp/

    Body: { "report_id": <int>, "email": "<patient email>" } OR { "token": "<uuid>" }

    Validates the inputs, generates a fresh OTP, updates/persists it, and
    dispatches the verification email.
    """

    permission_classes = []   # No authentication required for this endpoint

    def post(self, request):
        from datetime import timedelta
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        report = serializer.validated_data["report"]
        email = serializer.validated_data["email"]
        old_otp_record = serializer.validated_data.get("otp_record")

        otp = generate_otp()

        if old_otp_record:
            old_otp_record.otp_hash = hash_otp(otp)
            old_otp_record.is_verified = False
            old_otp_record.is_used = False
            old_otp_record.expires_at = timezone.now() + timedelta(minutes=10)
            old_otp_record.save()
            otp_record = old_otp_record
        else:
            otp_record = ReportAccessOTP.objects.create(
                report=report,
                email=email,
                otp_hash=hash_otp(otp),
            )

        try:
            send_otp_email(
                recipient_email=email,
                otp=otp,
                token=str(otp_record.token),
            )
        except Exception:
            if not old_otp_record:
                otp_record.delete()
            return Response(
                {"detail": "Failed to send OTP email. Please try again."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {
                "detail": "OTP sent successfully. Please check your email.",
                "token": str(otp_record.token),
            },
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(APIView):
    """
    POST /api/verify-otp/

    Body: { "token": "<uuid>", "otp": "<6-digit code>" }

    Validates the token, checks expiry, compares hashed OTP,
    and marks the record as verified + used on success.
    """

    permission_classes = []

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data["token"]
        plain_otp = serializer.validated_data["otp"]

        try:
            otp_record = ReportAccessOTP.objects.select_related("report").get(
                token=token
            )
        except ReportAccessOTP.DoesNotExist:
            return Response(
                {"detail": "Invalid or unrecognised token."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if otp_record.is_used:
            return Response(
                {"detail": "This token has already been used."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp_record.is_expired:
            return Response(
                {"detail": "OTP has expired. Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not verify_otp(plain_otp, otp_record.otp_hash):
            return Response(
                {"detail": "Incorrect OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_record.is_verified = True
        otp_record.is_used = True
        otp_record.save(update_fields=["is_verified", "is_used"])

        return Response(
            {
                "detail": "OTP verified successfully.",
                "token": str(otp_record.token),
            },
            status=status.HTTP_200_OK,
        )


class ReportAccessView(APIView):
    """
    GET /api/report/<uuid:token>/

    Returns the report only when the supplied token has been
    previously verified (is_verified=True) and belongs to this patient.
    """

    permission_classes = []

    def get(self, request, token):
        try:
            otp_record = ReportAccessOTP.objects.select_related(
                "report", "report__doctor"
            ).get(token=token)
        except ReportAccessOTP.DoesNotExist:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not otp_record.is_verified:
            return Response(
                {"detail": "Token has not been verified. Please complete OTP verification."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ReportSerializer(otp_record.report)
        return Response(serializer.data, status=status.HTTP_200_OK)