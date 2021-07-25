# Django
from django.urls import path
from django.views.generic.base import RedirectView

# Locals
from . import views

favicon_view = RedirectView.as_view(url="/static/pages/favicons/favicon.ico", permanent=True)


app_name = "pages"
urlpatterns = [
    path("<slug:slug>/", views.PageView.as_view(), name="page"),
    path(
        "<slug:slug>/success",
        views.PageView.as_view(),
        {"success": True},
        name="page_success",
    ),
    path("<slug:slug>/list", views.ModuleListView.as_view(), name="modulelist"),
    path(r"favicon\.ico", favicon_view),
    path("", views.HomePage.as_view(), name="home"),
]
