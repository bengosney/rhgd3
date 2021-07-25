# Django
from django.contrib import admin

# First Party
from modulestatus.admin import statusDateRangeAdmin

# Locals
from .models import message


class messageAdmin(statusDateRangeAdmin, admin.ModelAdmin):
    model = message

    list_display = ("title", "dismissible")


admin.site.register(message, messageAdmin)
