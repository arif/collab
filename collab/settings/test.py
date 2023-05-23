from .base import *  # noqa: f403

AUTH_USER_FACTORY = 'users.factories.UserFactory'

MEDIA_ROOT = os.path.join(BASE_DIR, 'test-media')  # noqa: f405
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
