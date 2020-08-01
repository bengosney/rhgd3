# Django
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.static import serve

# Locals
from .sitemaps import sitemaps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('garden/', include('gardens.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('pages.urls')),
]

if settings.DEBUG:
    urlpatterns += url(r'^media/(?P<path>.*)$',
                       serve,
                       {'document_root': settings.MEDIA_ROOT,
                        'show_indexes': True}),
