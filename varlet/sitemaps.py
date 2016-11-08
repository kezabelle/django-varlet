# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from django.contrib.sitemaps import Sitemap


class PageSitemap(Sitemap):

    @property
    def model(self):
        return swapper.load_model("varlet", "Page")

    def items(self):
        return self.model.objects.filter()
