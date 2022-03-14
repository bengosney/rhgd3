# Django

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

# Locals
from .models import message


def dismiss(request, slug):
    try:
        m = message.objects.get(slug=slug)
        request.session[m.session_key] = True
        request.session.modified = True
    except ObjectDoesNotExist:
        pass

    url = request.headers.get("Referer", "/")

    return HttpResponseRedirect(url)
