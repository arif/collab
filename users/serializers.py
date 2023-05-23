from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login

from jwt import decode as jwt_decode
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.serializers import \
    TokenObtainPairSerializer as DefaultTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import \
    TokenRefreshSerializer as DefaultTokenRefreshSerializer
from rest_framework_simplejwt.serializers import \
    TokenVerifySerializer as DefaultTokenVerifySerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from .exceptions import RefreshTokenInvalid, TokenCouldNotBeVerified

UserModel = get_user_model()


class TokenObtainPairSerializer(DefaultTokenObtainPairSerializer):
    username_field = UserModel.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(trim_whitespace=False)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        token['email_validation_time'] = user.email_validation_time.isoformat() \
            if user.email_validation_time else None
        token['full_name'] = user.get_full_name()
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['date_joined'] = user.date_joined.isoformat()
        token['permissions'] = list(user.get_all_permissions())

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        del data['refresh']
        del data['access']

        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class TokenRefreshSerializer(DefaultTokenRefreshSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        access_token = refresh.access_token
        pk = access_token['id']

        try:
            user = UserModel.objects.get(pk=pk)
        except UserModel.DoesNotExist:  # pragma: no cover
            raise RefreshTokenInvalid

        access_token['email'] = user.email
        access_token['email_validation_time'] = user.email_validation_time.isoformat()\
            if user.email_validation_time else None
        access_token['full_name'] = user.get_full_name()
        access_token['first_name'] = user.first_name
        access_token['last_name'] = user.last_name
        access_token['date_joined'] = user.date_joined.isoformat()
        access_token['permissions'] = list(user.get_all_permissions())

        data = {'access_token': str(access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:  # pragma: no cover
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh_token'] = str(refresh)
        return data


class TokenVerifySerializer(DefaultTokenVerifySerializer):
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            UntypedToken(attrs['token'])
        except TokenError:  # pragma: no cover
            raise InvalidToken

        data = jwt_decode(attrs['token'], settings.SECRET_KEY, algorithms=['HS256'])
        user_id = data.get('user_id', None)

        try:
            UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:  # pragma: no cover
            raise TokenCouldNotBeVerified

        data = {
            'id': data['id'],
            'email': data['email'],
            'email_validation_time': data['email_validation_time'],
            'full_name': data['full_name'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'date_joined': data['date_joined'],
            'permissions': data['permissions'],
        }

        return data
