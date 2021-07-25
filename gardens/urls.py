# Django
from django.urls import path

# Locals
from . import views

app_name = "gardens"

urlpatterns = [
    path("", views.GardenList.as_view(), name="GardenList"),
    path("<slug:slug>", views.GardenDetail.as_view(), name="GardenDetail"),
    path(
        "filter/<slug:slug>/",
        views.GardenListFiltered.as_view(),
        name="GardenListFiltered",
    ),
    path(
        "maintenance/<slug:slug>/",
        views.MaintenanceItemDetailView.as_view(),
        name="MaintenanceItemDetailView",
    ),
]
