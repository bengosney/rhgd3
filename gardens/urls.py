
from django.conf.urls import url

from . import views

app_name = 'gardens'
urlpatterns = [
    url(r'^$',
        views.GardenList.as_view(),
        name='GardenList'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.GardenDetail.as_view(),
        name='GardenDetail'),
]
