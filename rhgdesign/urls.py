# Django
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.static import serve

# Locals
from .sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("garden/", include("gardens.urls")),
    path("banners/", include("banner_messages.urls", namespace="banner_messages")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += (
        path(
            "media/(?P<path>.*)",
            serve,
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
        ),
    )
