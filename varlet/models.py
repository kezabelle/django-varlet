# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
from django import forms
from django.apps import apps
from django.core.exceptions import ValidationError

try:
    from django.urls import reverse, resolve, Resolver404
except ImportError:
    from django.core.urlresolvers import reverse, resolve, Resolver404
from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
import swapper
from templatefinder import find_all_templates, template_choices


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class BasePage(models.Model):
    url = models.CharField(max_length=2048, unique=True, verbose_name=_('url'), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def clean(self):
        super(BasePage, self).clean()
        self.url = self.url.strip('/')
        application_root = reverse('page_detail', kwargs={'remaining_path': ''})
        if application_root.strip('/') == '':
            # Don't allow URLs like /admin/ IF the app is mounted at /
            # as the "last resort" in the project's main urlconf.
            this_url = self.get_absolute_url()
            this_url_stripped = this_url.rstrip('/')
            for url in (this_url, this_url_stripped):
                try:
                    resolved = resolve(url)
                except Resolver404:
                    continue
                else:
                    if resolved.url_name != 'page_detail':
                        msg = ("Pages cannot be created for URLs which are already "
                               "handled by another application")
                        if resolved.app_names:
                            first_name = resolved.app_names[0]
                            try:
                                appconf = apps.get_app_config(first_name)
                            except LookupError:
                                pass
                            else:
                                app = appconf.verbose_name
                                msg = "{0} called '{1}'".format(msg, app)
                        msg2 = "{0}, the URL already points to {1}".format(msg, resolved.view_name)
                        logger.info(msg2)
                        raise ValidationError({'url': msg})
        return None

    def get_template_names(self):
        msg = ("Concrete (non-abstract) classes should implement this to "
               "return a list of template paths that may be discovered by "
               "the Django template loaders")
        raise NotImplementedError(msg)

    def get_absolute_url(self):
        url = reverse('page_detail', kwargs={'remaining_path': self.url})
        return url

    def __str__(self):
        return self.get_absolute_url()

    class Meta:
        abstract = True


class TemplateField(models.CharField):
    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(TemplateField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(TemplateField, self).deconstruct()
        kwargs['path'] = self.path
        return name,path, args, kwargs

    def formfield(self, **kwargs):
        found_templates = find_all_templates(pattern=self.path)
        choices  = tuple(template_choices(found_templates))
        defaults = {
            'choices': choices,
            'coerce': self.to_python,
            'form_class': forms.TypedChoiceField,
        }
        return super(models.CharField, self).formfield(**defaults)


class Page(BasePage):
    template = TemplateField(path='varlet/pages/layouts/*.html',
                             max_length=255,
                                verbose_name=_('template'),
                                help_text=_('templates may affect the display '
                                            'of this page on the website.'))

    def get_template_names(self):
        return [self.template]

    class Meta:
        swappable = swapper.swappable_setting('varlet', 'Page')
