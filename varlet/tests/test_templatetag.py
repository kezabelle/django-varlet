# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import pytest
import swapper
from varlet.templatetags.page_tags import get_page


@pytest.mark.django_db
def test_template_tag_loads_ok():
    Page = swapper.load_model('varlet', 'Page')
    page = Page(url='/this/is/a/test/', template='varlet/pages/layouts/test_template.html')
    page.full_clean()
    page.save()
    x = get_page('/this/is/a/test/')
    assert x == page


def test_template_tag_handles_invalid_lookups():
    x = get_page('/this/is/&a/test/')
    assert x is None


@pytest.mark.django_db
def test_template_tag_handles_nonexistant_items():
    Page = swapper.load_model('varlet', 'Page')
    page = Page(url='/this/is/a/test/', template='varlet/pages/layouts/test_template.html')
    page.full_clean()
    page.save()
    x = get_page('/this/////')
    assert x is None
