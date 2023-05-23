from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import BasePermission

UserModel = get_user_model()


class IsSuperuser(BasePermission):
    message = _('You are not authorized to perform this action.')
    code = 'not_authorized'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsAdminOrSuperuser(BasePermission):
    message = _('You do not have permission to perform this action.')
    code = 'permission_denied'

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))
