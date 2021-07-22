# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party
from modulestatus.models import statusDateMixin, statusDateRangeMixin, statusMixin


class statusDateRangeTest(statusDateRangeMixin):
    title = models.CharField(_("Title"), max_length=150)

    class Meta:
        app_label = "statusDateRangeTestApp"


class statusDateTest(statusDateMixin):
    title = models.CharField(_("Title"), max_length=150)

    class Meta:
        app_label = "statusDateTestApp"


class statusTest(statusMixin):
    title = models.CharField(_("Title"), max_length=150)

    class Meta:
        app_label = "statusTestApp"
