# Standard Library
from datetime import datetime

# Django
from django.db import models
from django.db.models.query import QuerySet

# Locals
from . import ModelStatus


class statusManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=ModelStatus.LIVE_STATUS)


class statusDateManager(statusManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(published__lte=datetime.now().date())


class statusDateRangeManager(statusManager):
    def get_queryset(self) -> QuerySet:
        filter = {
            "published_from__lte": datetime.today().date(),
            "published_to__gte": datetime.now().date(),
        }


        return super().get_queryset().filter(**filter)


try:
    # Third Party
    from polymorphic_tree.managers import PolymorphicMPTTModelManager

    class PolymorphicMPTTStatusManager(PolymorphicMPTTModelManager):
        def get_queryset(self):
            return super().get_queryset().filter(status=ModelStatus.LIVE_STATUS)


except ImportError:
    pass
