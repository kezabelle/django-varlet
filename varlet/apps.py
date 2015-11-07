# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _


class PageAppConfig(AppConfig):
    name = "varlet"
    label = "pages"
    verbose_name = _("Pages")

    def ready(self):
        from .listeners import maybe_update_homepage
        from .models import Page
        pre_save.connect(maybe_update_homepage, sender=Page,
                 dispatch_uid='maybe_update_homepage')
