from django import template

from websettings.models import setting

register = template.Library()

@register.assignment_tag
def websetting(title):
    return setting.getValue(title)
