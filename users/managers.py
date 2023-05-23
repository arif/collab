from django.contrib.auth.models import BaseUserManager
from django.db import models

__all__ = ['UserManager']


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class CollabUserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, **extra):
        if not email:
            raise ValueError('Users must have an email address.')
        if not password:
            raise ValueError('Users must have set a password.')
        if not first_name or not last_name:
            raise ValueError('Users must have their first name and last name.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password, **extra):
        extra.setdefault('is_staff', False)
        extra.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, password, **extra)

    def create_superuser(self, email, first_name, last_name, password, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self._create_user(email, first_name, last_name, password, **extra)


UserManager = CollabUserManager.from_queryset(UserQuerySet)
