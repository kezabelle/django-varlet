# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import pytest
import swapper
from django.contrib.sitemaps.views import sitemap
from django.utils.encoding import force_text

from varlet.sitemaps import PageSitemap


@pytest.mark.django_db
def test_rendering_sitemaps(rf):
    Page = swapper.load_model('varlet', 'Page')
    pages = [Page.objects.create(url=str(x), template="admin/filter.html") for x in range(1, 5)]
    sm = PageSitemap()
    response = sitemap(rf.get('/'), sitemaps={'pages': sm})
    response.render()
    assert '<loc>http://example.com/3/</loc>' in force_text(response.content)
    assert '<loc>http://example.com/2/</loc>' in force_text(response.content)
    assert '<loc>http://example.com/1/</loc>' in force_text(response.content)
