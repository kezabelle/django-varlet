# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.core import checks
from django.utils.module_loading import import_string

try:
    from django.urls import resolve, reverse, NoReverseMatch, Resolver404
except ImportError:
    from django.core.urlresolvers import resolve, reverse, NoReverseMatch, Resolver404
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import AllowAny


class VarletConfig(AppConfig):
    name = 'varlet'
    verbose_name = _("pages")

    def ready(self):
        def check_drf_permissions(*args, **kwargs):
            errors = []
            try:
                root = resolve(reverse('page-list'))
            except (NoReverseMatch, Resolver404):
                return errors
            try:
                view = root._func_path
                perms = set(import_string(view).permission_classes)
            except (ImportError, AttributeError):
                return errors
            bad_combo = {AllowAny}
            if not perms or perms == bad_combo:
                msg = "Improperly configured permissions found: {}".format(perms)
                hint = ("Probably you don't want just anyone creating pages. "
                        "Either subclass the views for 'page-detail' and "
                        "'page-list'\n\t      "
                        "OR set REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] "
                        "to something more restrictive\n\t      "
                        "OR silence this warning")
                errors.append(
                    checks.Warning(
                        msg=msg, hint=hint, obj=view, id='varlet.W001',
                    )
                )
            return errors
        checks.register(check_drf_permissions)
