from urllib.parse import parse_qs

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

UserModel = get_user_model()


@database_sync_to_async
def get_user(validated_token):
    try:
        user = UserModel.objects.get(id=validated_token['user_id'])
        return user

    except UserModel.DoesNotExist:
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()

        try:
            token = parse_qs(scope['query_string'].decode('utf8'))['token'][0]
        except KeyError:
            return None

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError):
            return None
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            scope['user'] = await get_user(validated_token=decoded_data)
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
