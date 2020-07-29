# Django
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class setting(models.Model):
    title = models.CharField(max_length=150)
    value = models.CharField(max_length=150)

    def __str__(self):
        return "{}: {}".format(self.title, self.value)

    @staticmethod
    def getValue(title):
        try:
            obj = setting.objects.get(title=title)
            return obj.value
        except ObjectDoesNotExist:
            obj = setting(title=title, value="")
            obj.save()
            return ""
