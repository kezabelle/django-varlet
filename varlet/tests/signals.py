# -*- coding: utf-8 -*-
from collections import namedtuple
from django.db.models.signals import pre_save
from django.test import TestCase as TestCaseUsingDB
from varlet.listeners import maybe_update_homepage
from varlet.models import Page


Result = namedtuple('Result', 'pk homepage')


class SignalsTestCase(TestCaseUsingDB):
    def test_without_signal(self):
        pre_save.disconnect(maybe_update_homepage, sender=Page,
                            dispatch_uid='slugpage_maybe_update_homepage')
        page = Page(title='test', template='test', slug='test',
                    is_homepage=True)
        page.save()
        page2 = Page(title='test2', template='test2', slug='test2',
                     is_homepage=False)
        page2.save()
        # now two pages, the first of which is the homepage.
        results = tuple(Result(pk=x.pk, homepage=x.is_homepage)
                        for x in Page.objects.all().order_by('pk'))
        self.assertEqual(results, (
            Result(pk=1, homepage=True),
            Result(pk=2, homepage=False),
        ))
        page2.is_homepage = True
        page2.save()
        # now two pages, but both are the homepage.
        results = tuple(Result(pk=x.pk, homepage=x.is_homepage)
                        for x in Page.objects.all().order_by('pk'))
        self.assertEqual(results, (
            Result(pk=1, homepage=True),
            Result(pk=2, homepage=True),
        ))

    def test_pre_save_signal_to_update_homepage(self):
        pre_save.disconnect(maybe_update_homepage, sender=Page,
                            dispatch_uid='slugpage_maybe_update_homepage')
        pre_save.connect(maybe_update_homepage, sender=Page,
                         dispatch_uid='TESTING_maybe_update_homepage')
        
        page = Page(title='test', template='test', slug='test',
                    is_homepage=True)
        page.save()
        # initially only one page, which is the homepage
        results = tuple(Result(pk=x.pk, homepage=x.is_homepage)
                        for x in Page.objects.all().order_by('pk'))
        self.assertEqual(results, (
            Result(pk=1, homepage=True),
        ))

        page2 = Page(title='test2', template='test2', slug='test2',
                     is_homepage=False)
        page2.save()
        # now two pages, the first of which is the homepage.
        results = tuple(Result(pk=x.pk, homepage=x.is_homepage)
                        for x in Page.objects.all().order_by('pk'))
        self.assertEqual(results, (
            Result(pk=1, homepage=True),
            Result(pk=2, homepage=False),
        ))

        page2.is_homepage = True
        page2.save()
        # now two pages, and we should've switched the homepage via the signal
        results = tuple(Result(pk=x.pk, homepage=x.is_homepage)
                        for x in Page.objects.all().order_by('pk'))
        self.assertEqual(results, (
            Result(pk=1, homepage=False),
            Result(pk=2, homepage=True),
        ))
        pre_save.disconnect(maybe_update_homepage, sender=Page,
                            dispatch_uid='TESTING_maybe_update_homepage')
