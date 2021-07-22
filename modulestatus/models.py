# Future

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Locals
from . import ModelStatus
from .managers import statusDateManager, statusDateRangeManager, statusManager


class statusMixin(models.Model):
    status = models.IntegerField(_("Status"), choices=ModelStatus.STATUS_CHOICES, default=ModelStatus.LIVE_STATUS)

    objects = statusManager()
    admin_objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.status}"


class statusDateMixin(statusMixin):
    published = models.DateField(_("Published"))

    objects = statusDateManager()

    class Meta:
        abstract = True


class statusDateRangeMixin(statusMixin):
    published_from = models.DateField(_("Published from"))
    published_to = models.DateField(_("Published to"))

    objects = statusDateRangeManager()

    class Meta:
        abstract = True
