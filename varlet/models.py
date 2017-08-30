# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
import re

import unicodedata

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from templateselector.fields import TemplateField
try:
    from django.urls import reverse, resolve, Resolver404, NoReverseMatch
except ImportError:  # pragma: no cover
    from django.core.urlresolvers import reverse, resolve, Resolver404
from django.db import models
from django.utils.html import escape
from django.utils.six import python_2_unicode_compatible
try:
    from django.utils.six.moves.urllib.parse import urlsplit
except ImportError:  # pragma: no cover
    from urllib.parse import urlsplit
from django.utils.translation import ugettext_lazy as _
import swapper


logger = logging.getLogger(__name__)


replace_spaces_re = re.compile('\s+')
replace_multi_spaces_re = re.compile('-{2,}')


class BasePageQuerySet(QuerySet):
    def get_by_natural_key(self, url):
        return self.get(url=url)


class URLPathField(models.CharField):
    description = _("String (up to %(max_length)s) with additional validation "
                    "that the input looks like a URL Path")
    def to_python(self, value):
        value = super(URLPathField, self).to_python(value)
        tidying_url = value.strip().strip('/')
        tidying_url = unicodedata.normalize('NFKC', tidying_url)
        tidying_url = replace_spaces_re.sub('-', tidying_url)
        tidying_url = replace_multi_spaces_re.sub('-', tidying_url)
        parsed_url = urlsplit(tidying_url).path.strip('/')
        if parsed_url != tidying_url:
            raise ValidationError("Unsafe characters detected")
        if escape(parsed_url) != parsed_url:
            raise ValidationError("Unsafe characters detected")
        return parsed_url


@python_2_unicode_compatible
class BasePage(models.Model):
    url = URLPathField(max_length=2048, unique=True, verbose_name=_('URL'), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = BasePageQuerySet.as_manager()

    def clean(self):
        super(BasePage, self).clean()
        try:
            this_url = self.get_absolute_url()
        except NoReverseMatch:
            # If we hit this exception, it means the field (URLPathField) didn't
            # validate, so contains invalid characters that the urlconf also
            # doesn't permit.
            return None
        application_root = reverse('page-detail', kwargs={'url': ''})
        if application_root.strip('/') in ('', "%2F"):
            # Don't allow URLs like /admin/ IF the app is mounted at /
            # as the "last resort" in the project's main urlconf.
            this_url_stripped = this_url.rstrip('/')
            for url in (this_url, this_url_stripped):
                try:
                    resolved = resolve(url)
                except Resolver404:
                    continue
                else:
                    if resolved.url_name not in ('page-detail', 'page-list'):
                        msg = ("Pages cannot be created for URLs which are already "
                               "handled by another application")
                        if hasattr(resolved, 'app_names') and resolved.app_names:
                            app_name = resolved.app_names[0]
                        elif hasattr(resolved, 'app_name'):
                            app_name = resolved.app_name
                        else:
                            app_name = None
                        if app_name is not None:
                            try:
                                appconf = apps.get_app_config(app_name)
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
        url = reverse('page-detail', kwargs={'url': self.url})
        if url == "/%2F": # we're mounted at root, and this is the root page?
            return "/"
        return url.replace("//", "/")

    def __str__(self):
        try:
            return self.get_absolute_url()
        except NoReverseMatch:
            return "Invalid URL"

    def natural_key(self):
        return (self.url,)

    class Meta:
        abstract = True


class Page(BasePage):
    template = TemplateField(match=r'^varlet/pages/layouts/.+\.html$',
                             help_text=_('templates may affect the display '
                                         'of this page on the website.'))

    def get_template_names(self):
        return [self.template]

    class Meta:
        swappable = swapper.swappable_setting('varlet', 'Page')
        ordering = ('-modified',)
