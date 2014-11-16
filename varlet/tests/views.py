# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.template.response import TemplateResponse
from django.test import TestCase as TestCaseUsingDB
from django.test.utils import override_settings
from django.test.client import RequestFactory
from model_mommy import mommy
from varlet.models import Page
from varlet.views import Homepage, PageDetail


class HomepageViewTestCase(TestCaseUsingDB):
    @override_settings(DEBUG=True)
    def test_when_no_homepage_shows_debug_page_in_debug(self):
        home = reverse('pages:index')
        request = RequestFactory().get(home)
        view = Homepage.as_view()
        with self.assertNumQueries(2):
            response = view(request)
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, TemplateResponse)

    def test_when_no_homepage_throws_404(self):
        home = reverse('pages:index')
        request = RequestFactory().get(home)
        view = Homepage.as_view()
        with self.assertRaises(Http404):
            with self.assertNumQueries(1):
                view(request)

    def test_when_homepage_exists(self):
        home = reverse('pages:index')
        request = RequestFactory().get(home)
        view = Homepage.as_view()
        mommy.make(Page, is_homepage=True, template='test.html')
        with self.assertNumQueries(1):
            response = view(request)
        self.assertIn('Allow', response)
        self.assertEqual(response['Allow'], 'GET, HEAD, OPTIONS, POST')
        self.assertIsInstance(response, TemplateResponse)
        with self.assertRaises(TemplateDoesNotExist):
            response.render()


class NormalPageViewTestCase(TestCaseUsingDB):
    def test_redirect_to_index_if_homepage(self):
        url = reverse('pages:view', kwargs={'slug': 'test'})
        request = RequestFactory().get(url)
        mommy.make(Page, slug='test', is_homepage=True)
        view = PageDetail.as_view()
        with self.assertNumQueries(1):
            response = view(request, slug='test')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], reverse('pages:index'))

    def test_normal_page(self):
        url = reverse('pages:view', kwargs={'slug': 'test2'})
        request = RequestFactory().get(url)
        view = PageDetail.as_view()
        mommy.make(Page, slug='test2', is_homepage=False)
        with self.assertNumQueries(1):
            response = view(request, slug='test2')
        self.assertIn('Allow', response)
        self.assertEqual(response['Allow'], 'GET, HEAD, OPTIONS, POST')
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(TemplateDoesNotExist):
            response.render()
