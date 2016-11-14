# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from varlet.urls import urlpatterns as varlet_urls
from varlet.sitemaps import PageSitemap

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap.xml$', sitemap, {'sitemaps': {'pages': PageSitemap()}}, name='xml_sitemap'),
    url(r'^', include(varlet_urls)),
]
