# Django
from django.contrib import admin

# Third Party
from adminsortable2.admin import SortableAdminMixin
from image_cropping import ImageCroppingMixin
from polymorphic_tree.admin import PolymorphicMPTTChildModelAdmin, PolymorphicMPTTParentModelAdmin

# First Party
from modulestatus.admin import statusAdmin

# Locals
from .models import ContactSubmission, Empty, ExternalLink, HomePageHeader, HomePagePod, ModuleList, Page, node


class BaseChildAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = (
        None,
        {
            "fields": ("parent", "status", "title"),
        },
    )

    SEO_FIELDSET = (
        "SEO",
        {
            "classes": ("grp-collapse grp-closed",),
            "fields": ("title_tag", "meta_description"),
        },
    )

    NAV_FIELDSET = (
        "Navigation",
        {
            "classes": ("grp-collapse grp-closed",),
            "fields": ("nav_title", "nav_icon", "nav_icon_only", "active_url_helper"),
        },
    )

    base_model = node
    base_fieldsets = (
        GENERAL_FIELDSET,
        NAV_FIELDSET,
        SEO_FIELDSET,
    )

    class Media:
        js = ("pages/js/ckeditor.js",)


class BaseChildNoSEOAdmin(BaseChildAdmin):
    pass


class ModuleListAdmin(BaseChildAdmin):
    pass


class ExternalLinkAdmin(BaseChildAdmin):
    pass


class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = node
    child_models = (
        Page,
        Empty,
        ModuleList,
        ExternalLink,
    )

    list_display = (
        "title",
        "actions_column",
    )


class ContactAdmin(admin.ModelAdmin):
    model = ContactSubmission

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class HomePageHeaderAdmin(SortableAdminMixin, ImageCroppingMixin, admin.ModelAdmin):
    model = HomePageHeader
    list_display = (
        "admin_image",
        "strapline",
    )

    class Media:
        js = ("pages/js/ckeditor.js",)


class HomePagePodAdmin(SortableAdminMixin, statusAdmin, admin.ModelAdmin):
    model = HomePagePod

    class Media:
        js = ("pages/js/ckeditor.js",)


admin.site.register(node, TreeNodeParentAdmin)
admin.site.register(ContactSubmission, ContactAdmin)
admin.site.register(HomePageHeader, HomePageHeaderAdmin)
admin.site.register(HomePagePod, HomePagePodAdmin)
admin.site.register(Page, BaseChildAdmin)
admin.site.register(Empty, BaseChildNoSEOAdmin)
admin.site.register(ModuleList, ModuleListAdmin)
admin.site.register(ExternalLink, BaseChildAdmin)
