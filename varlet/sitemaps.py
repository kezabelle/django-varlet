# -*- coding: utf-8 -*-
import logging
from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from .models import Page


logger = logging.getLogger(__name__)


class MinimalPageSitemap(Sitemap):

    def items(self):
        raise NotImplementedError("Subclasses should implement this")

    def lastmod(self, obj):
        return obj.modified

    def changefreq(self, obj):
        datediff = timezone.now() - obj.modified
        if datediff.days < 3:
            return 'daily'
        if datediff.days <= 7:
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


class PageSitemap(MinimalPageSitemap):
    # __slots__ = ('model',)

    def __init__(self, model=None):
        self.model = model or Page

    def items(self):
        return self.model.objects.all()
