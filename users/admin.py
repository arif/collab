from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.forms import UserChangeForm, UserCreationForm
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add/change user instances.
    form = UserChangeForm
    add_form = UserCreationForm

    # The template for add form view.
    add_form_template = None

    # The fields to be used in displaying User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (_('Permissions'), {
            'fields': ('groups', 'user_permissions', 'is_active', 'is_staff', 'is_superuser', ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'email_validation_time', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'first_name', 'last_name', 'password', 'password_repeat', ),
        }),
    )
    list_display = ('first_name', 'last_name', 'email', 'language', 'is_active', 'is_staff', 'is_superuser', )
    list_filter = ('is_active', 'is_staff', 'is_superuser', )
    search_fields = ('first_name', 'last_name', 'email', )
    ordering = ('-date_joined', )
    filter_horizontal = ('groups', 'user_permissions', )
