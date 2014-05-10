# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


def maybe_update_homepage(sender, instance, **kwargs):
    """
    If the current ``instance`` has been marked as the homepage, get rid
    of any others. To avoid any further signals being thrown, this uses the
    queryset update() method.

    ..note::
        At a minimum, this triggers **one** query to discover other homepages.
        At a maximum, it'll do **two**, to discover and update those homepages.

    :rtype: None
    """
    if instance.is_homepage:
        other_homepage = sender.objects.filter(is_homepage=True)

        if instance.pk is not None:
            logger.debug("Instance already exists, so exclude it from the "
                         "search for other existing homepages")
            other_homepage = other_homepage.exclude(pk=instance.pk)

        if other_homepage.exists():
            logger.info("Another homepage already exists, so we need to "
                        "turn it off.")
            other_homepage.update(is_homepage=False)
            return True
    return False
