# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from classytags.arguments import Argument, StringArgument
from classytags.core import Options
from classytags.helpers import AsTag
from django import template
from varlet.models import Page


register = template.Library()
logger = logging.getLogger(__name__)


class GetPage(AsTag):
    """
    Hey you need to put a Page instance into the context? Sweet, let's do this::

        {% load get_page %}
        {% get_page 'slug' as outvar %}
        {{ outvar.title }}
    """
    name = 'get_page'
    options = Options(
        StringArgument('slug', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=True),
    )

    def get_value(self, context, slug):
        try:
            return Page.objects.get(slug=slug)
        except (Page.DoesNotExist, Page.MultipleObjectsReturned) as e:
            debug_enabled = settings.DEBUG and settings.TEMPLATE_DEBUG
            if debug_enabled and settings.DEBUG_PROPAGATE_EXCEPTIONS:
                raise
            logger.error("Page for slug: {slug!s} isn't in the "
                         "database".format(slug=slug), exc_info=1)
            return None
register.tag(GetPage)
