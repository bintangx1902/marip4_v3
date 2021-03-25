from django.urls import path
from .sitemaps import *
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'book': BookSitemap,
}

con = {'sitemaps': sitemaps}

app_name = 'site'

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap')
]
