from django.urls import path
from .views import SendOTPView, VerifyOTPView, ReportAccessView, CreateReportView

urlpatterns = [
    path("send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("report/<uuid:token>/", ReportAccessView.as_view(), name="report-access"),
    path("reports/create/", CreateReportView.as_view(), name="create-report"),
]