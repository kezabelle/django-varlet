# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import swapper
from django import template
from django.core.exceptions import MultipleObjectsReturned, ValidationError

register = template.Library()

@register.simple_tag(takes_context=False)
def get_page(path):
    Page = swapper.load_model('varlet', 'Page')
    field = Page._meta.get_field('url')
    try:
        cleaned_path = field.to_python(path)
    except ValidationError:
        return None
    try:
        return Page.objects.get(url=cleaned_path)
    except (Page.DoesNotExist, MultipleObjectsReturned):
        return None
