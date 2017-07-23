import os

from datetime import date

from django.db import models
from django_extensions.db import fields
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from image_cropping import ImageRatioField
from ckeditor_uploader.fields import RichTextUploadingField as RichTextField

from modulestatus.models import statusMixin

class WorkType(statusMixin, models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title
    

class Garden(statusMixin, models.Model):
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=250, blank=True)
    work_type = models.ManyToManyField(WorkType, blank=True)
    description = RichTextField(_("Body"))

    slug = fields.AutoSlugField(populate_from='title')
    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Garden')
        verbose_name_plural = _('Gardens')

    @property
    def url(self):
        return reverse_lazy('gardens:GardenDetail')



class GardenPhoto(models.Model):
    garden = models.ForeignKey(Garden)
    image = models.ImageField(upload_to='uploads/gardens')

    main = ImageSpecField(source='image',
                          processors=[ResizeToFit(600, 400)],
                          format='JPEG',
                          options={'quality': 70})

    thumbnail = ImageRatioField('image', '375x300')

    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return os.path.basename(self.image.url)

    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
