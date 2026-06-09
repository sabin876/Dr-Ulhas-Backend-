from django.db import migrations

def remove_duplicates(apps, schema_editor):
    ReportAccessOTP = apps.get_model('Report', 'ReportAccessOTP')
    
    # Get all (email, report_id) combinations
    seen = set()
    duplicates = []
    
    for otp in ReportAccessOTP.objects.all().order_by('-created_at'):
        key = (otp.email, otp.report_id)
        if key in seen:
            duplicates.append(otp.id)
        else:
            seen.add(key)
    
    # Delete older duplicates, keep the newest
    if duplicates:
        ReportAccessOTP.objects.filter(id__in=duplicates).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0001_initial'),  # or whatever your last migration is
    ]

    operations = [
        migrations.RunPython(remove_duplicates),
    ]