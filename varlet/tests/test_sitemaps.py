# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import timedelta
import pytest
import swapper
from django.contrib.sitemaps.views import sitemap
from django.utils import timezone
from django.utils.encoding import force_text

from varlet.sitemaps import PageSitemap


@pytest.mark.django_db
def test_rendering_sitemaps(rf):
    Page = swapper.load_model('varlet', 'Page')
    pages = [Page.objects.create(url=str(x), template="varlet/pages/layouts/test_template.html") for x in range(1, 5)]
    sm = PageSitemap()
    response = sitemap(rf.get('/'), sitemaps={'pages': sm})
    response.render()
    assert '<loc>http://example.com/3/</loc>' in force_text(response.content)
    assert '<loc>http://example.com/2/</loc>' in force_text(response.content)
    assert '<loc>http://example.com/1/</loc>' in force_text(response.content)


@pytest.mark.parametrize("recently,priority", (
    (timezone.now() - timedelta(minutes=60), 1.0),
    (timezone.now() - timedelta(days=10), 0.8),
    (timezone.now() - timedelta(days=20), 0.6),
))
def test_rendering_sitemaps_highest_priorty(recently, priority):
    Page = swapper.load_model('varlet', 'Page')
    page1 = Page(url='test', template="varlet/pages/layouts/test_template.html", modified=recently)
    sm = PageSitemap()
    assert sm.priority(obj=page1) == priority
