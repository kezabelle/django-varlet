# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

import pytest
import swapper
from django.utils.encoding import force_text

@pytest.yield_fixture
def pages():
    PAGES = (
        '/this/is/a/test/',
        '/this/is/a',
        '/this/is/',
        '/this/',
        '/test/',
        '/unrelated/',
        '/contains/test/in/it/'
    )
    Page = swapper.load_model('varlet', 'Page')
    pages = []
    for page in PAGES:
        page = Page(url=page, template='admin/filter.html')
        page.full_clean()
        page.save()
        pages.append(page)
    yield pages

@pytest.mark.django_db
def test_autocomplete_typeahead(admin_client, pages):
    resp = admin_client.get('/admin/varlet/page/urls/', data={'q': 'this/is/a/test'})
    data = json.loads(force_text(resp.content))
    assert data == {
        'count': 6,
        'results': [{'name': 'this/is/a'},
                    {'name': 'this/is'},
                    {'name': 'this'},
                    {'name': 'test'},
                    {'name': 'contains/test/in/it'},
                    {'name': 'unrelated'}]
    }

@pytest.mark.django_db
def test_autocomplete_typeahead2(admin_client, pages):
    resp = admin_client.get('/admin/varlet/page/urls/', data={'q': 'this/is'})
    data = json.loads(force_text(resp.content))
    assert data == {
        'count': 3,
        'results':  [{'name': 'this/is/a'},
                     {'name': 'this/is/a/test'},
                     {'name': 'this'}]
    }

@pytest.mark.django_db
def test_autocomplete_typeahead3(admin_client, pages):
    resp = admin_client.get('/admin/varlet/page/urls/', data={'q': 'test'})
    data = json.loads(force_text(resp.content))
    assert data == {
        'count': 2,
        'results': [{'name': 'this/is/a/test'},
                    {'name': 'contains/test/in/it'}]
    }
