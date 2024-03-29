# Standard Library
import os

# Django
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Third Party
from ckeditor_uploader.fields import RichTextUploadingField as RichTextField
from django_extensions.db import fields
from image_cropping import ImageRatioField

# First Party
from modulestatus.models import statusMixin


class MaintenanceItem(statusMixin, models.Model):
    title = models.CharField(max_length=150)
    short_description = models.CharField(_("Short Description"), max_length=150, blank=True)
    description = RichTextField(_("Description"))

    slug = fields.AutoSlugField(populate_from="title")

    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("position",)
        verbose_name = _("Maintenance Item")
        verbose_name_plural = _("Maintenance Items")

    @property
    def url(self):
        if self.slug == "":
            self._meta.get_field("slug").create_slug(self, True)
            self.save()

        return reverse_lazy("gardens:MaintenanceItemDetailView", kwargs={"slug": self.slug})

    @property
    def list_description(self):
        if self.short_description != "":
            return f"<p>{self.short_description}</p>"
        else:
            return self.description


class MaintenancePhoto(models.Model):
    MaintenanceItem = models.ForeignKey(MaintenanceItem, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/maintenancephotos")

    large = ImageRatioField("image", "675x500")
    thumbnail = ImageRatioField("image", "170x145")

    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return os.path.basename(self.image.url)

    class Meta:
        ordering = ("position",)
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")


class WorkType(statusMixin, models.Model):
    title = models.CharField(max_length=150)
    slug = fields.AutoSlugField(populate_from="title")
    description = RichTextField(_("Description"))

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("position",)
        verbose_name = _("Work Type")
        verbose_name_plural = _("Work Types")

    def __str__(self):
        return self.title


class Garden(statusMixin, models.Model):
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=250, blank=True)
    work_type = models.ManyToManyField(WorkType, blank=True)

    short_description = models.CharField(_("Short Description"), max_length=150, blank=True)
    description = RichTextField(_("Body"))

    slug = fields.AutoSlugField(populate_from="title")
    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("position",)
        verbose_name = _("Garden")
        verbose_name_plural = _("Gardens")

    @property
    def url(self):
        return reverse_lazy("gardens:GardenDetail", kwargs={"slug": self.slug})

    @property
    def gardenphoto_hero_set(self):
        return self.gardenphoto_set.filter(is_hero=True)


class GardenPhoto(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/gardens")

    main = ImageRatioField("image", "600x400")
    thumbnail = ImageRatioField("image", "160x145")
    hero = ImageRatioField("image", "1600x484")
    is_hero = models.BooleanField(_("Hero Image"))

    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return os.path.basename(self.image.url)

    class Meta:
        ordering = ("position",)
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")

    def save(self, *args, **kwargs):
        if self.is_hero:
            try:
                temp = GardenPhoto.objects.get(is_hero=True, garden=self.garden)
                if self != temp:
                    temp.is_hero = False
                    temp.save()
            except GardenPhoto.DoesNotExist:
                pass
        super().save(*args, **kwargs)
