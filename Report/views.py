from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.contrib import messages
from django.views import View

from .models import Report, ReportAccessOTP
from .serializers import (
    CreateReportSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
    ReportSerializer,
)
from .services.otp_service import OTPService
from .services.email_service import EmailService


class SendOTPAdminView(View):
    """
    Admin action to send OTP for a specific report
    Accessed via: /admin/report/report/<id>/send-otp/
    """
    
    def get(self, request, report_id):
        try:
            report = Report.objects.get(id=report_id)
            
            # Create OTP record
            otp_record, otp = OTPService.create_otp_record(report, report.patient_email)
            
            # Queue email task
            email_sent = EmailService.send_otp_email(
                email=report.patient_email,
                otp=otp,
                token=otp_record.token,
                report_id=report.id
            )
            
            if email_sent:
                messages.success(
                    request,
                    f"OTP sent successfully to {report.patient_email}. Token: {otp_record.token}"
                )
            else:
                otp_record.delete()
                messages.error(
                    request,
                    "Failed to send OTP email. Please try again."
                )
            
            # Redirect back to report admin change page
            return redirect(f"/admin/Report/report/{report_id}/change/")
        
        except Report.DoesNotExist:
            messages.error(request, "Report not found")
            return redirect("/admin/Report/report/")
        
        except Exception as e:
            messages.error(request, f"Error sending OTP: {str(e)}")
            return redirect(f"/admin/Report/report/{report_id}/change/")


class CreateReportView(APIView):
    """
    POST /api/reports/create/

    Doctor-only endpoint (must be authenticated).
    Creates a Report WITHOUT automatically sending OTP.
    Use SendOTPView to send OTP after report is created.

    Body: { "patient_email": "patient@example.com", "content": "...", "report_file": <file> }

    Response 201:
    {
        "detail": "Report created successfully. Use Send OTP button to send verification link.",
        "report": { id, doctor, patient_email, content, created_at },
        "message": "Click 'Send OTP' button in admin to email the patient"
    }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Bind the authenticated doctor to the report
        report = serializer.save(doctor=request.user)

        return Response(
            {
                "detail": "Report created successfully. Use Send OTP button to send verification link.",
                "report": ReportSerializer(report).data,
                "message": "Click 'Send OTP' button in admin to email the patient"
            },
            status=status.HTTP_201_CREATED,
        )


class SendOTPView(APIView):
    """
    POST /api/send-otp/

    Body: { "report_id": <int>, "email": "<patient email>" }

    Validates that the report exists and the email matches, then
    generates a fresh OTP + token, persists the hashed OTP, and
    dispatches the verification email via Celery task.
    """

    permission_classes = []   # No authentication required for this endpoint

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        report = serializer.validated_data["report"]
        email = serializer.validated_data["email"]

        # Create OTP record
        otp_record, otp = OTPService.create_otp_record(report, email)

        # Queue email task
        email_sent = EmailService.send_otp_email(
            email=email,
            otp=otp,
            token=otp_record.token,
            report_id=report.id
        )

        if not email_sent:
            otp_record.delete()
            return Response(
                {"detail": "Failed to send OTP email. Please try again."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {
                "detail": "OTP sent successfully. Please check your email.",
                "token": str(otp_record.token),
                "email": email,
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

        # Validate and mark used
        is_valid, error_message = OTPService.validate_and_mark_used(otp_record, plain_otp)
        
        if not is_valid:
            return Response(
                {"detail": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

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