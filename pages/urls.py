from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

favicon_view = RedirectView.as_view(url='/static/pages/favicons/favicon.ico', permanent=True)


app_name = 'pages'
urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', views.PageView.as_view(), name='page'),
    url(r'^(?P<slug>[\w-]+)/success$', views.PageView.as_view(), {'success': True}, name='page_success'),
    url(r'^(?P<slug>[\w-]+)/list$', views.ModuleListView.as_view(), name='modulelist'),
    url(r'^favicon\.ico$', favicon_view),
    url(r'^$', views.HomePage.as_view(), name='home'),
]
