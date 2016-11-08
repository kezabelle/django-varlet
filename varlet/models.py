# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import swapper
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BasePage(models.Model):
    url = models.CharField(max_length=2048, unique=True, verbose_name=_('url'), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def clean(self):
        super(BasePage, self).clean()
        self.url = self.url.strip('/')

    def get_template_names(self):
        msg = ("Concrete (non-abstract) classes should implement this to "
               "return a list of template paths that may be discovered by "
               "the Django template loaders")
        raise NotImplementedError(msg)

    def is_root(self):
        return self.url == ''

    class Meta:
        abstract = True


class Page(BasePage):
    template = models.CharField(max_length=255,
                                verbose_name=_('template'),
                                help_text=_('templates may affect the display '
                                            'of this page on the website.'))

    def get_template_names(self):
        return [self.template]

    class Meta:
        swappable = swapper.swappable_setting('varlet', 'Page')
