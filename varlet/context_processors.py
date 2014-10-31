# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from .models import Page


logger = logging.getLogger(__name__)


def get_homepage(request):
    # TODO: make this lazy but only evaluated once, if possible.
    def wrapped_db_query():
        try:
            return Page.objects.get_homepage()
        except (Page.DoesNotExist, Page.MultipleObjectsReturned) as e:
            debug_enabled = settings.DEBUG and settings.TEMPLATE_DEBUG
            if debug_enabled and settings.DEBUG_PROPAGATE_EXCEPTIONS:
                raise
            logger.error("Unable to find a canonical homepage", exc_info=1)
            return None
    return {
        'HOMEPAGE': wrapped_db_query(),
    }
