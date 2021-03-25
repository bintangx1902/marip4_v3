from django.contrib.sitemaps import Sitemap
from backend.models import Book


class BookSitemap(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return Book.objects.all()

    def lastmod(self, obj):
        return obj.upload_date
