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

    
class GardenAdmin(
        SortableAdminMixin,
        statusAdmin,
        ImageCroppingMixin,
        admin.ModelAdmin):
    model = models.Garden
    inlines = [GardenPhotoInline]
    #list_display = ('title', 'gardentype')
    list_per_page = 25

    class Media:
        js = ('pages/js/ckeditor.js',)

        
class MaintenancePhotoInline(
        #SortableInlineAdminMixin,
        ImageCroppingMixin,
        admin.TabularInline):
    model = models.MaintenancePhoto
    extra = 3

        
class MaintenanceItemAdmin(
        SortableAdminMixin,
        statusAdmin,
        ImageCroppingMixin,
        admin.ModelAdmin):
    model = models.MaintenanceItem
    inlines = [MaintenancePhotoInline]
    list_per_page = 25

    class Media:
        js = ('pages/js/ckeditor.js',)

        
class TypeAdmin(admin.ModelAdmin):
    model = models.WorkType

    class Media:
        js = ('pages/js/ckeditor.js',)

    
    
admin.site.register(models.Garden, GardenAdmin)
admin.site.register(models.WorkType, TypeAdmin)
admin.site.register(models.MaintenanceItem, MaintenanceItemAdmin)
