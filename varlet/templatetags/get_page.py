# -*- coding: utf-8 -*-
from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag
from django import template
from varlet.models import Page

register = template.Library()


class GetPage(AsTag):
    """
    Hey you need to put a Page instance into the context? Sweet, let's do this::

        {% load get_page %}
        {% get_page 'slug' as outvar %}
        {{ outvar.title }}
    """
    name = 'get_page'
    options = Options(
        Argument('slug', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=True),
    )

    def get_value(self, context, slug):
        try:
            return Page.objects.get(slug=slug)
        except Page.DoesNotExist, Page.MultipleObjectsReturned:
            return None
register.tag(GetPage)
