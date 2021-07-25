# Future
from __future__ import annotations

# Standard Library
import importlib
from datetime import datetime

# Django
from django.db import models
from django.urls import reverse
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _

# Third Party
from ckeditor_uploader.fields import RichTextUploadingField as RichTextField
from django_extensions.db import fields
from image_cropping import ImageRatioField
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey

# First Party
from modulestatus.models import statusMixin

# Locals
from .decorators import get_registered_list_views


class node(PolymorphicMPTTModel, statusMixin):
    ICONS = [
        ("twitter-square", "Twitter"),
        ("facebook-square", "Facebook"),
        ("instagram", "Instagram"),
        ("linkedin-square", "LinkedIn"),
    ]

    parent = PolymorphicTreeForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="children",
        verbose_name=_("parent"),
        on_delete=models.SET_NULL,
    )
    title = models.CharField(_("Title"), max_length=200)

    nav_title = models.CharField(_("Navigation Title"), max_length=200, blank=True, default="")
    nav_icon = models.CharField(_("Navigation Icon"), choices=ICONS, max_length=200, blank=True, default="")
    nav_icon_only = models.BooleanField(_("Icon Only"), default=False)

    slug = fields.AutoSlugField(populate_from="title")

    title_tag = models.CharField(_("Title Tag"), max_length=200, blank=True, default="")
    meta_description = models.TextField(blank=True, default="")
    active_url_helper = models.CharField(max_length=255, blank=True, default="")
    is_home_page = models.BooleanField(default=False)

    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("Site node")
        verbose_name_plural = _("Site nodes")

    def __str__(self):
        return self.title

    @property
    def url(self):
        if self.is_home_page:
            return "/"

        try:
            url = reverse("pages:%s" % self.__class__.__name__.lower(), kwargs={"slug": self.slug})
        except BaseException:
            url = reverse("pages:page", kwargs={"slug": self.slug})

        return url

    def nav_class(self):
        classes = [self.__class__.__name__]

        if self.nav_icon:
            classes.append("icon-{}".format(str(self.nav_icon)))

        if self.nav_icon_only:
            classes.append("icon-only")

        return " ".join(classes)

    @property
    def nav_title_actual(self):
        if self.nav_title:
            return self.nav_title
        else:
            return self.title

    def save(self, *args, **kwargs):
        if self.is_home_page:
            try:
                temp = node.objects.get(is_home_page=True)
                if self != temp:
                    temp.is_home_page = False
                    temp.save()
            except node.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    @staticmethod
    def get_nav_tree():
        pass


class Empty(node):
    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("Empty Item")
        verbose_name_plural = _("Empty Items")

    def __unicode__(self):
        return "%s - Empty Node" % self.title

    @property
    def url(self):
        return "#%s" % self.slug


class ExternalLink(node):
    URL = models.URLField(_("URL"))

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("External Link")
        verbose_name_plural = _("External Links")

    @property
    def url(self):
        return self.URL


class Page(node):
    FORM_CHOICES = (
        ("ContactForm", "Contact Form"),
        ("FosteringForm", "Fostering Form"),
    )

    body = RichTextField(_("Body"))
    show_map = models.BooleanField(_("Show map"), default=False)
    form = models.CharField(max_length=100, blank=True, default="", choices=FORM_CHOICES)
    success_message = RichTextField(_("Success Message"), blank=True, default="")

    def getFormClass(self):
        # Locals
        from . import forms

        return getattr(forms, self.form)

    @property
    def success_url(self):
        return reverse("pages:page_success", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")


class ModuleList(node):
    module = models.CharField(
        _("Module"),
        max_length=200,
    )

    body = RichTextField(_("Body"), null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field("module").choices = lazy(get_registered_list_views, list)()

    class Meta:
        verbose_name = _("Module List")
        verbose_name_plural = _("Module Lists")

    def get_view_object(self):
        module_name, class_name = self.module.rsplit(".", 1)
        view_class = getattr(importlib.import_module(module_name), class_name)
        return view_class()


class ContactSubmission(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    phone = models.CharField(_("Phone"), max_length=100, blank=True, default="")
    email = models.EmailField(_("Email"))
    enquiry = models.TextField(_("Enquiry"))
    consent = models.BooleanField(
        _("I am over 18 and I give consent for data I enter into this form to be use to respond to my enquiry.")
    )

    created = fields.CreationDateTimeField()

    def __str__(self):
        return self.name


class HomePageHeader(models.Model):
    image = models.ImageField(upload_to="images")
    cropped = ImageRatioField("image", "1600x484")
    strapline = models.CharField(_("Strap Line"), max_length=200)
    itemlink = models.ForeignKey(node, null=True, blank=True, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    start = models.DateField(null=True, default=None)
    end = models.DateField(null=True, default=None)

    def __str__(self):
        return self.strapline

    def admin_image(self):
        return '<img src="%s" height="75"/>' % self.image.url

    admin_image.allow_tags = True

    class Meta:
        ordering = ("position",)

    @classmethod
    def getCurrentImage(cls) -> HomePageHeader | None:
        today = datetime.today()

        image = cls.objects.filter(
            start__month__lte=today.month,
            start__day__lte=today.day,
            end__month__gte=today.month,
            end__day__gte=today.day,
        ).first()

        if image is None:
            image = cls.objects.all().order_by("-start").first()

        return image


class HomePagePod(statusMixin, models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=350)

    image = models.ImageField(upload_to="uploads/homepagepods", blank=True, default="")

    link = models.ForeignKey(node, on_delete=models.CASCADE)

    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("position",)
        verbose_name = _("Home Page Pod")
        verbose_name_plural = _("Home Page Pods")

    def url(self):
        return self.link.url
