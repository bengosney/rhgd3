# Django
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Third Party
from django_extensions.db import fields

# First Party
from modulestatus.models import statusDateRangeMixin


class message(statusDateRangeMixin, models.Model):
    title = models.CharField(_("Title"), max_length=150)
    message = models.TextField(_("Message"), max_length=1280)
    dismissible = models.BooleanField(_("Dismissible"), default=True)

    slug = fields.AutoSlugField(populate_from="title")

    def __str__(self):
        return f"{self.title}"

    @property
    def dismiss_url(self):
        return reverse("banner_messages:dismiss", kwargs={"slug": self.slug})

    @property
    def session_key(self):
        return f"message-{self.slug}-dismissed"

    @classmethod
    def get_messages(cls, session):
        return [o for o in cls.objects.all() if not session.get(o.session_key, False) or not o.dismissible]
