from django.contrib import admin

# Register your models here.
from .models import Report, ReportAccessOTP

admin.site.register(Report)
admin.site.register(ReportAccessOTP)
