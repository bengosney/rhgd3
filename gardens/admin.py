# Django
from django import forms
from django.contrib import admin

# Third Party
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from image_cropping import ImageCroppingMixin

# First Party
from modulestatus.admin import statusAdmin

# Locals
from . import models


class GardenPhotoInline(SortableInlineAdminMixin, ImageCroppingMixin, admin.TabularInline):
    model = models.GardenPhoto
    extra = 3


class GardenAdmin(SortableAdminMixin, statusAdmin, ImageCroppingMixin, admin.ModelAdmin):
    model = models.Garden
    inlines = [GardenPhotoInline]
    list_per_page = 25

    class Media:
        js = ("pages/js/ckeditor.js",)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "short_description":
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)

        return formfield


class MaintenancePhotoInline(ImageCroppingMixin, admin.TabularInline):
    model = models.MaintenancePhoto
    extra = 3


class MaintenanceItemAdmin(SortableAdminMixin, statusAdmin, ImageCroppingMixin, admin.ModelAdmin):
    model = models.MaintenanceItem
    inlines = [MaintenancePhotoInline]
    list_per_page = 25

    class Media:
        js = ("pages/js/ckeditor.js",)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "short_description":
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)

        return formfield


class TypeAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = models.WorkType

    class Media:
        js = ("pages/js/ckeditor.js",)


admin.site.register(models.Garden, GardenAdmin)
admin.site.register(models.WorkType, TypeAdmin)
admin.site.register(models.MaintenanceItem, MaintenanceItemAdmin)
