# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase as TestCaseUsingDB
from django.test.utils import override_settings
from django.test.client import RequestFactory
from model_mommy import mommy
from varlet.context_processors import get_homepage
from varlet.models import Page


class GetHomepageTestCase(TestCaseUsingDB):
    def setUp(self):
        self.rf = RequestFactory()

    def test_admin_prevents_putting_into_context(self):
        admin_index = reverse('admin:index')
        req = self.rf.get('{admin}/some/other/app/'.format(admin=admin_index))
        mommy.make(Page, is_homepage=True)
        with self.assertNumQueries(0):
            result = get_homepage(request=req)
        self.assertIn('HOMEPAGE', result)
        self.assertIsNone(result['HOMEPAGE'])

    def test_getting_homepage(self):
        req = self.rf.get('/yay/')
        page = mommy.make(Page, is_homepage=True)
        with self.assertNumQueries(1):
            result = get_homepage(request=req)
        self.assertIn('HOMEPAGE', result)
        self.assertIsNotNone(result['HOMEPAGE'])
        self.assertEqual(page, result['HOMEPAGE'])

    def test_getting_nonexistant_homepage(self):
        req = self.rf.get('/yay/')
        with self.assertNumQueries(1):
            result = get_homepage(request=req)
        self.assertIn('HOMEPAGE', result)
        self.assertIsNone(result['HOMEPAGE'])

    @override_settings(DEBUG=True, TEMPLATE_DEBUG=True,
                       DEBUG_PROPAGATE_EXCEPTIONS=True)
    def test_getting_nonexistant_homepage_when_developing(self):
        req = self.rf.get('/yay/')
        with self.assertNumQueries(1):
            with self.assertRaises(ObjectDoesNotExist):
                get_homepage(request=req)
