# Django
from django.contrib.sitemaps import Sitemap

# First Party
from gardens.models import Garden, MaintenanceItem
from pages.models import Empty, ExternalLink, node


class rhgdSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def location(self, obj):
        return obj.url

    def lastmod(self, obj):
        return obj.modified


class GardenSitemap(rhgdSitemap):
    priority = 0.75

    def items(self):
        return Garden.objects.all()


class MaintenanceSitemap(rhgdSitemap):
    priority = 1

    def items(self):
        return MaintenanceItem.objects.all()


class PageSitemap(rhgdSitemap):
    def items(self):
        return node.objects.not_instance_of(ExternalLink, Empty)


sitemaps = {
    "pages": PageSitemap,
    "gardens": GardenSitemap,
    "maintenance": MaintenanceSitemap,
}
