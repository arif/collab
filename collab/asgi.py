"""
ASGI config for collab project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from documents.middleware import JwtAuthMiddlewareStack
from documents.routing import websocket_urlpatterns

settings = os.environ['DJANGO_SETTINGS']

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', f'collab.settings.{settings}'
)

django.setup()

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': JwtAuthMiddlewareStack(
            URLRouter(websocket_urlpatterns),
        ),
    }
)
