from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('First name'), max_length=150)
    last_name = models.CharField(_('Last name'), max_length=150)
    email = models.EmailField(_('Email'), unique=True, max_length=255)
    email_validation_time = models.DateTimeField(_('Email validation time'), blank=True, null=True, auto_now_add=False)
    date_joined = models.DateTimeField(_('Date joined'), default=now)
    is_active = models.BooleanField(_('Is active'), default=True)
    is_staff = models.BooleanField(_('Is staff'), default=False)
    language = models.CharField(_('Language'), max_length=8, default=settings.LANGUAGE_CODE)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', ]

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('-date_joined', )

    def __str__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_language(self):
        return self.language
