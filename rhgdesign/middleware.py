# Standard Library
import logging

# Django
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)


class ClacksOverhead:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["x-clacks-overhead"] = "GNU Terry Pratchett"

        return response


class ProperURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        current_site = get_current_site(request)

        host = request.get_host()
        valid_hosts = ["testserver", current_site.domain]
        if not settings.DEBUG and host not in valid_hosts and not request.path.startswith("/admin"):
            redir = f"https://{current_site.domain}{request.path}"
            logger.error(f"Incorect url hit: {request.get_host()}, redirecting to {redir}")

            return HttpResponseRedirect(redir)

        return response
