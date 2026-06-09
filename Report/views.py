from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.contrib import messages
from django.views import View
import logging

from .models import Report, ReportAccessOTP
from .serializers import (
    CreateReportSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
    ReportSerializer,
)
from .services.otp_service import OTPService
from .services.email_service import EmailService

logger = logging.getLogger(__name__)


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
                    f"✅ OTP sent successfully to {report.patient_email}"
                )
            else:
                otp_record.delete()
                messages.error(
                    request,
                    "❌ Failed to send OTP email. Please try again."
                )
            
            # Redirect back to report admin change page
            return redirect(f"/admin/Report/report/{report_id}/change/")
        
        except Report.DoesNotExist:
            messages.error(request, "❌ Report not found")
            return redirect("/admin/Report/report/")
        
        except Exception as e:
            logger.error(f"Error in SendOTPAdminView: {str(e)}")
            messages.error(request, f"❌ Error sending OTP: {str(e)}")
            return redirect(f"/admin/Report/report/{report_id}/change/")


class CreateReportView(APIView):
    """
    POST /api/reports/create/

    Doctor-only endpoint (must be authenticated).
    Creates a Report WITHOUT automatically sending OTP.

    Request:
    {
        "patient_email": "patient@example.com",
        "content": "Medical diagnosis...",
        "report_file": <file>
    }

    Response 201:
    {
        "detail": "Report created successfully.",
        "report": { id, doctor, patient_email, content, created_at }
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
                "detail": "✅ Report created successfully.",
                "report": ReportSerializer(report).data
            },
            status=status.HTTP_201_CREATED,
        )


class SendOTPView(APIView):
    """
    POST /api/send-otp/

    Send OTP to patient's email using email + report_id.

    Request:
    {
        "report_id": 5,
        "email": "patient@gmail.com"
    }

    Response 200:
    {
        "detail": "✅ OTP sent successfully to patient@gmail.com",
        "email": "patient@gmail.com",
        "message": "Check your email for the OTP"
    }
    """
    permission_classes = []

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        report = serializer.validated_data["report"]
        email = serializer.validated_data["email"]

        try:
            # Delete old unused OTP for this email+report combo
            ReportAccessOTP.objects.filter(
                email=email,
                report=report,
                is_used=False
            ).delete()

            # Create new OTP record
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
                    "detail": f"✅ OTP sent successfully to {email}",
                    "email": email,
                    "report_id": report.id,
                    "message": "Check your email for the OTP"
                },
                status=status.HTTP_200_OK,
            )
        
        except Exception as e:
            logger.error(f"Error in SendOTPView: {str(e)}")
            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerifyOTPView(APIView):
    """
    POST /api/verify-otp/

    Verify OTP using email + report_id + OTP code.
    No token needed - just use email!

    Request:
    {
        "email": "patient@gmail.com",
        "report_id": 5,
        "otp": "123456"
    }

    Response 200:
    {
        "detail": "✅ OTP verified successfully.",
        "email": "patient@gmail.com",
        "report": {
            "id": 5,
            "doctor_name": "Dr. Rajesh",
            "patient_email": "patient@gmail.com",
            "content": "Medical diagnosis...",
            "report_file": "/media/reports/report_5.pdf",
            "created_at": "2026-06-09T10:00:00Z"
        }
    }
    """
    permission_classes = []

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            otp_record = serializer.validated_data["otp_record"]
            report = serializer.validated_data["report"]
            email = serializer.validated_data["email"]

            # Mark OTP as verified and used
            otp_record.is_verified = True
            otp_record.is_used = True
            otp_record.save()

            logger.info(f"OTP verified for {email}, report {report.id}")

            return Response(
                {
                    "detail": "✅ OTP verified successfully.",
                    "email": email,
                    "report_id": report.id,
                    "report": ReportSerializer(report).data
                },
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            logger.error(f"Error in VerifyOTPView: {str(e)}")
            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReportAccessView(APIView):
    """
    GET /api/report/

    Access report using email + report_id.
    Only works if OTP has been verified for this email.

    Request:
    GET /api/report/?email=patient@gmail.com&report_id=5

    Response 200:
    {
        "id": 5,
        "doctor_name": "Dr. Rajesh",
        "patient_email": "patient@gmail.com",
        "content": "Medical diagnosis...",
        "report_file": "/media/reports/report_5.pdf",
        "created_at": "2026-06-09T10:00:00Z"
    }
    """
    permission_classes = []

    def get(self, request):
        email = request.query_params.get('email')
        report_id = request.query_params.get('report_id')

        if not email or not report_id:
            return Response(
                {"detail": "Missing email or report_id query parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            report = Report.objects.get(pk=report_id)
        except Report.DoesNotExist:
            return Response(
                {"detail": "❌ Report not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if report.patient_email.lower() != email.lower():
            return Response(
                {"detail": "❌ Email does not match report's patient email."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            otp_record = ReportAccessOTP.objects.get(
                email=email,
                report=report
            )
        except ReportAccessOTP.DoesNotExist:
            return Response(
                {"detail": "❌ No verification record found. Please verify OTP first."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not otp_record.is_verified:
            return Response(
                {"detail": "❌ Email has not been verified. Please complete OTP verification first."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if otp_record.is_expired:
            return Response(
                {"detail": "❌ Verification has expired. Please request a new OTP."},
                status=status.HTTP_403_FORBIDDEN,
            )

        logger.info(f"Report accessed by {email} for report {report.id}")

        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)