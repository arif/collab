from django.conf import settings
from django.contrib.auth import get_user_model

from jwt import decode as jwt_decode
from rest_framework_simplejwt.authentication import \
    JWTAuthentication as DefaultJWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

UserModel = get_user_model()


class JWTAuthentication(DefaultJWTAuthentication):
    """
    An authentication plugin that provides verifying and authenticates requests through
    a JSON web token provided in a request header.
    """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:  # pragma: no cover
            return None

        validated_token = self.get_validated_token(raw_token)

        decoded_token = jwt_decode(raw_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_id = decoded_token.get('user_id', None)

        try:
            user = UserModel.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):  # pragma: no cover
            user = None

        if user is None:  # pragma: no cover
            raise InvalidToken

        return self.get_user(validated_token), validated_token
