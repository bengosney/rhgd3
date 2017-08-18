
from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', views.PageView.as_view(), name='page'),
    url(r'^(?P<slug>[\w-]+)/success$', views.PageView.as_view(), {'success': True}, name='page_success'),
#    url(r'^(?P<slug>[\w-]+)/list/(?P<filter_type>[\w-]+)/(?P<filter_val>[\w-]+)$',
#        views.ModuleListView.as_view(),
#        name='modulelistfiltered'),
    url(r'^(?P<slug>[\w-]+)/list$', views.ModuleListView.as_view(), name='modulelist'),
    url(r'^$', views.HomePage.as_view(), name='home'),
]
