# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from django.contrib.sitemaps import Sitemap
from django.utils import timezone


__all__ = ['PageSitemap']


class BasePageSitemap(Sitemap):
    @property
    def model(self):
        return swapper.load_model("varlet", "Page")

    def items(self):
        return self.model.objects.all()


class PageSitemap(BasePageSitemap):
    def lastmod(self, obj):
        return obj.modified

    def changefreq(self, obj):
        datediff = timezone.now() - obj.modified
        if datediff.days < 7:
            return 'daily'
        if datediff.days <= 14:
            return 'weekly'
        return 'monthly'

    def priority(self, obj):
        """
        The farther down the rabbit hole we go, the lest important the pages,
        right?
        """
        final_priority = 1.0
        freq = self.changefreq(obj=obj)
        if freq == 'weekly':
            final_priority = 0.8
        elif freq == 'monthly':
            final_priority = 0.6
        return final_priority
