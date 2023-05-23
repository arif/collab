from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from utils.permissions import IsSuperuser

from .authentication import JWTAuthentication
from .serializers import (TokenObtainPairSerializer, TokenRefreshSerializer,
                          TokenVerifySerializer)
from .utils.jwt import get_token_for_user

UserModel = get_user_model()

sensitive_post_parameters_method = method_decorator(
    sensitive_post_parameters(
        'password', 'password_repeat', 'old_password',
    )
)


class LoginView(TokenObtainPairView):
    """
    Endpoint Name: Login (Get token)
    Endpoint Code: A1
    """
    serializer_class = TokenObtainPairSerializer
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAsView(GenericAPIView):
    """
    Endpoint Code: A2
    Endpoint Name: Login as
    """

    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsSuperuser, )

    def post(self, request, *args, **kwargs):
        user_id = request.query_params.get('id', None)
        if user_id is not None:
            try:
                user = UserModel.objects.get(pk=int(user_id), is_active=True)
            except UserModel.DoesNotExist:
                user = None

            if user is not None:
                token = get_token_for_user(user)
                return Response(data=token, status=status.HTTP_200_OK)
            else:
                data = {
                    'message': _('User not found with given id.'),
                    'code': 'user_not_found',
                }
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        else:
            data = {
                'message': _('You need to specify user_id'),
                'code': 'missing_user_id'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(TokenRefreshView):
    """
    Endpoint Name: Refresh token
    Endpoint Code: A3
    """
    serializer_class = TokenRefreshSerializer
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)


class VerifyTokenView(TokenVerifyView):
    """
    Endpoint Name: Verify token
    Endpoint Code: A4
    """
    serializer_class = TokenVerifySerializer
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
