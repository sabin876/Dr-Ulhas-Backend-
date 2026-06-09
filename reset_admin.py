import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
password = 'adminpassword123'

try:
    u = User.objects.get(username=username)
    u.set_password(password)
    u.save()
    print(f"SUCCESS: Updated existing '{username}' user password to '{password}'")
except User.DoesNotExist:
    User.objects.create_superuser(username, 'admin@drulhasorthopedic.com', password)
    print(f"SUCCESS: Created new superuser '{username}' with password '{password}'")
