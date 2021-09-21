from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class StaticViewsSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"
    def items(self):
        return [
            'home',
        ]
    def location(self, item):
        return reverse(item)

class productViewsSitemap(Sitemap):
    def items(self):
        return Product.objects.all()

