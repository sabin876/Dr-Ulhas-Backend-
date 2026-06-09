from django.urls import path
from Report.views import (
    SendOTPView,
    VerifyOTPView,
    ReportAccessView,
    CreateReportView,
)

app_name = 'report'

urlpatterns = [
    # API endpoints
    path('create/', CreateReportView.as_view(), name='create-report'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('report/', ReportAccessView.as_view(), name='report-access'),
]