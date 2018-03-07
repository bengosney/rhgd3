from django.contrib.sitemaps import Sitemap
from django.db.models import Q

from pages.models import Page, ModuleList, node, ExternalLink, Empty
from gardens.models import Garden, MaintenanceItem

class rhgdSitemap(Sitemap):
    changefreq = "monthly"
    priority = .5

    def location(self, obj):
        return obj.url

    def lastmod(self, obj):
        return obj.modified


class GardenSitemap(rhgdSitemap):
    def items(self):
        return Garden.objects.all()

class MaintenanceSitemap(rhgdSitemap):
    def items(self):
        return MaintenanceItem.objects.all()

    
class PageSitemap(rhgdSitemap):
    def items(self):
        return node.objects.not_instance_of(ExternalLink, Empty)

    
sitemaps = {
    'pages': PageSitemap,
    'gardens': GardenSitemap,
    'maintenance': MaintenanceSitemap,
}
