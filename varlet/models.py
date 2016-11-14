# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import swapper
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
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

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'remaining_path': self.url})

    def is_root(self):
        return self.url == ''

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
