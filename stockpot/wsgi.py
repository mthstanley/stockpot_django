"""
WSGI config for stockpot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stockpot.settings")

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(settings.BASE_DIR, settings.DOTENV_PATH))

application = get_wsgi_application()
