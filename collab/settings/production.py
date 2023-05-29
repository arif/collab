from .base import *

SENTRY_DSN = env('SENTRY_DSN')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                ('127.0.0.1', 6379)
            ],
        },
    },
}
