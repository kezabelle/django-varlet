# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import xml.etree.ElementTree as ET
import pytest
import swapper
from django.template import TemplateDoesNotExist
from django.urls import reverse
from django.utils.six.moves.urllib.parse import urlsplit


@pytest.mark.django_db
def test_page_fails_with_nonexistant_template(client):
    Page = swapper.load_model('varlet', 'Page')
    homepage = Page(url='', template='home.html')
    homepage.full_clean()
    homepage.save()
    with pytest.raises(TemplateDoesNotExist):
        client.get(homepage.get_absolute_url())



@pytest.mark.django_db
def test_page_renders_ok(client):
    Page = swapper.load_model('varlet', 'Page')
    homepage = Page(url='', template='admin/filter.html')
    homepage.full_clean()
    homepage.save()
    response = client.get(homepage.get_absolute_url())
    assert response.status_code == 200
    response.render()
    assert '<h3>' in response.content
    assert '<ul>' in response.content



@pytest.mark.django_db
def test_sitemap_includes_urls(client):
    Page = swapper.load_model('varlet', 'Page')
    pages = []
    for x in range(1, 5):
        page = Page(url=str(x), template='admin/filter.html')
        page.full_clean()
        page.save()
        pages.append(page)
    response = client.get(reverse('xml_sitemap'))
    assert response.status_code == 200

    response.render()
    etree = ET.fromstring(response.content)
    children = etree.getchildren()
    locs = [x.getchildren()[0] for x in children]
    urls = [x.text for x in locs]
    xml_paths = set(urlsplit(x).path for x in urls)

    page_paths = set(x.get_absolute_url() for x in pages)
    assert page_paths == xml_paths


@pytest.mark.django_db
def test_admin_doesnt_allow_other_urls_to_be_copied(admin_client):
    data = {
        'url': '/admin/varlet/page/',
        'template': 'varlet/pages/layouts/test_template.html'
    }
    url = reverse('admin:varlet_page_add')
    response = admin_client.post(url, data=data, follow=False)
    response.render()
    looking_for = ("Pages cannot be created for URLs which are already "
                   "handled by another application")
    assert looking_for in response.content


@pytest.mark.django_db
def test_admin_does_allow_unused_urls(admin_client):
    data = {
        'url': 'sitemap2.xml',
        'template': 'varlet/pages/layouts/test_template.html'
    }
    url = reverse('admin:varlet_page_add')
    response = admin_client.post(url, data=data, follow=False)
    assert response.status_code == 302
    assert response.url == reverse('admin:varlet_page_changelist')
