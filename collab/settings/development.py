import socket

from .base import *

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS = [
    '127.0.0.1',
    f'{ip[:-1]}1',
]
