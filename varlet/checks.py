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


@register('varlet', 'settings')
def check_for_request_context_processor(app_configs, **kwargs):
    from django.conf import settings
    errors = []
    missing = True
    hint = 'No context processor config found'
    if hasattr(settings, 'TEMPLATES') and len(settings.TEMPLATES) > 0:
        first = settings.TEMPLATES[0]
        found = (first['BACKEND'] == 'django.template.backends.django.DjangoTemplates' and
                 'OPTIONS' in first and
                 'context_processors' in first['OPTIONS'] and
                 'django.template.context_processors.request' in first['OPTIONS']['context_processors'])
        missing = not found
        hint = "Add it to your TEMPLATES['OPTIONS']['context_processors']"
    elif hasattr(settings, 'TEMPLATE_CONTEXT_PROCESSORS'):
        missing = ('django.core.context_processors.request' not in
                   settings.TEMPLATE_CONTEXT_PROCESSORS)
        hint = "Add it to your TEMPLATE_CONTEXT_PROCESSORS (ps: change to using TEMPLATES)"

    if missing:
        errors.append(Warning(
            "Need the `django.core.context_processors.request` to function correctly.",
            hint=hint,
            obj=__name__, id='varlet.W2'))
    return errors


class PageAdminConfigChecks(ModelAdminChecks):
    pass
