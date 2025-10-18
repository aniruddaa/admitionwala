from django.contrib.sitemaps import Sitemap
from .models import College

class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        return ['home', 'college_list']

    def location(self, item):
        if item == 'home':
            return '/'
        if item == 'college_list':
            return '/colleges/'

class CollegeSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return College.objects.all()

    def location(self, obj):
        return f'/college/{obj.id}/'

    def lastmod(self, obj):
        # no updated field, fallback to None
        return None
