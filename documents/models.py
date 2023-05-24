from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

UserModel = get_user_model()


class Document(TimeStampedModel):
    title = models.CharField(_('title'), blank=True, default='')
    content = models.TextField(_('content'), blank=True, default='')
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        editable=False,
        related_name='documents',
        verbose_name=_('author'),
    )

    def __str__(self):
        return self.title
