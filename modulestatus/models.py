# Future

# Django
from django.db import models

# Locals
from . import ModelStatus
from .managers import statusDateManager, statusManager


class statusMixin(models.Model):
    status = models.IntegerField(choices=ModelStatus.STATUS_CHOICES, default=ModelStatus.LIVE_STATUS)

    objects = statusManager()
    admin_objects = models.Manager()

    class Meta:
        abstract = True


class statusDateMixin(statusMixin):
    published = models.DateField()

    objects = statusDateManager()

    class Meta:
        abstract = True
