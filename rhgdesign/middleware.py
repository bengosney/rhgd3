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
        print('Clacks')
        response = self.get_response(request)

        response['x-clacks-overhead'] = 'GNU Terry Pratchett'

        return response


class ProperURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        current_site = get_current_site(request)

        print(request.path)
        if not settings.DEBUG and current_site.domain != request.get_host(
        ) and not request.path.startswith('/admin'):
            log_string = "Incorect url hit: {}".format(request.get_host())
            logger.error(log_string)
            print(log_string)
            redir = "https://{}{}".format(current_site.domain, request.path)

            return HttpResponseRedirect(redir)

        return response
