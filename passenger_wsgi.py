import os
import sys

# Add your project directory to the sys.path
# Change 'dr-ulhas-backend' to your project folder name if different
sys.path.insert(0, os.path.dirname(__file__))

# Set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

# Import the WSGI application
from core.wsgi import application
