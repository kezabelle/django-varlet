# -*- coding: utf-8 -*-
from django.contrib.admin.checks import ModelAdminChecks
from django.core.checks import Warning
from django.core.checks import register


@register('varlet', 'settings')
def check_for_template_display_names(app_configs, **kwargs):
    from django.conf import settings
    errors = []
    try:
        settings.TEMPLATE_DISPLAY_NAMES
    except AttributeError:
        errors.append(Warning(
            "Relying on auto-converting Page template names, because your "
            "settings doesn't define `TEMPLATE_DISPLAY_NAMES`",
            hint="set `TEMPLATE_DISPLAY_NAMES` to a dict or a"
                 "callable which returns a dict", obj=__name__,
            id='varlet.W1'))
    return errors


class PageAdminConfigChecks(ModelAdminChecks):
    pass
