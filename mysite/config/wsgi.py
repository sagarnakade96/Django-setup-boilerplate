"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


env = os.environ.get("MIRANA_APP", "local")
setting_file = f"config.settings.{str(env).lower()}"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)

application = get_wsgi_application()
