from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from image_cropping import ImageCroppingMixin

from modulestatus.admin import statusAdmin

import json
import os

from . import models

class GardenPhotoInline(
        SortableInlineAdminMixin,
        ImageCroppingMixin,
        admin.TabularInline):
    model = models.GardenPhoto
    extra = 3

    
class GardenAdmin(SortableAdminMixin, statusAdmin, admin.ModelAdmin):
    model = models.Garden
    inlines = [GardenPhotoInline]
    #list_display = ('title', 'gardentype')
    list_per_page = 25


class TypeAdmin(admin.ModelAdmin):
    model = models.WorkType


admin.site.register(models.Garden, GardenAdmin)
admin.site.register(models.WorkType, TypeAdmin)
