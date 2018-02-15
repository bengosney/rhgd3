
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
    url(r'^filter/(?P<slug>[\w-]+)/$',
        views.GardenListFiltered.as_view(),
        name='GardenListFiltered'),
    url(r'^maintenance/(?P<slug>[\w-]+)/$',
        views.MaintenanceItemDetailView.as_view(),
        name='MaintenanceItemDetailView'),
]
