"""
ASGI config for slippi_leaderboard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application


app_env = os.environ.get('APP_ENVIRONMENT', 'local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.{app_env}')

application = get_asgi_application()
