# -*- coding: utf-8 -*-
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase as TestCaseUsingDB
from model_mommy import mommy
from varlet.models import Page, PageTemplateError


try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    def get_user_model():
        return User


class ConcreteModelMethodsTestCase(TestCaseUsingDB):
    def test_get_menu_title_fallback_to_title(self):
        obj = mommy.prepare(Page, title='yay')
        self.assertEqual(obj.get_menu_title(), 'yay')

    def test_get_menu_title_with_defined_menutitle(self):
        obj = mommy.prepare(Page, title='yay', menu_title='not yay!')
        self.assertEqual(obj.get_menu_title(), 'not yay!')

    def test_absolute_url_normal_page(self):
        obj = mommy.prepare(Page, is_homepage=False, slug='test')
        expected_url = reverse('pages:view', kwargs={'slug': 'test'})
        self.assertEqual(obj.get_absolute_url(), expected_url)

    def test_absolute_url_homepage(self):
        obj = mommy.prepare(Page, is_homepage=True, slug='test')
        expected_url = reverse('pages:index')
        self.assertEqual(obj.get_absolute_url(), expected_url)

    def test_template_choices(self):
        self.assertEqual(tuple(Page.get_template_choices()),
                         (('varlet/pages/layouts/a.html', 'Template: a'),
                          ('varlet/pages/layouts/b.html', 'Another template: b')))

    def test_get_template_names_no_template(self):
        obj = mommy.prepare(Page, template=None)
        with self.assertRaises(PageTemplateError):
            obj.get_template_names()

    def test_get_template_names(self):
        obj = mommy.prepare(Page, template='test.html')
        self.assertEqual(obj.get_template_names(), ('test.html',))

    def test_anonymous_author(self):
        obj = mommy.prepare(Page)
        self.assertEqual(obj.author(), AnonymousUser())

    def test_anonymous_editor(self):
        obj = mommy.prepare(Page)
        self.assertEqual(obj.editor(), AnonymousUser())

    def test_proper_author(self):
        obj = mommy.make(Page)
        user = mommy.make(get_user_model())
        ct = ContentType.objects.get_for_model(obj).pk
        LogEntry.objects.create(content_type_id=ct, user=user,
                                action_flag=ADDITION, object_id=obj.pk)
        self.assertEqual(obj.author(), user)

    def test_proper_editor(self):
        obj = mommy.make(Page)
        user = mommy.make(get_user_model())
        user2 = mommy.make(get_user_model())
        ct = ContentType.objects.get_for_model(obj).pk
        LogEntry.objects.create(content_type_id=ct, user=user,
                                action_flag=ADDITION, object_id=obj.pk)
        LogEntry.objects.create(content_type_id=ct, user=user2,
                                action_flag=CHANGE, object_id=obj.pk)
        self.assertEqual(obj.editor(), user2)
