from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException


class TokenCouldNotBeVerified(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Token could not be verified.')
    default_code = 'token_could_not_be_verified'


class RefreshTokenInvalid(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _('Invalid token value given for refresh token.')
    default_code = 'invalid_refresh_token'
