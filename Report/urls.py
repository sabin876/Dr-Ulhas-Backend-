from django.urls import path
from .views import SendOTPView, VerifyOTPView, ReportAccessView

urlpatterns = [
    path("send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("report/<uuid:token>/", ReportAccessView.as_view(), name="report-access"),
]