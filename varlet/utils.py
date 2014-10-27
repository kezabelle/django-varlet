# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.text import capfirst
#from templatefinder.utils import find_all_templates
import re


to_space_re = re.compile(r'[^a-zA-Z0-9\-]+')


def _fix_display_title(template_path, template_map):
    if template_path in template_map:
        return template_map[template_path]
    # take the last part from the template path; works even if there is no /
    lastpart = template_path.rpartition('/')[-1]
    # take everything to the left of the rightmost . (the file extension)
    lastpart_minus_suffix = lastpart.rpartition('.')[0]
    # convert most non-alphanumeric characters into spaces, with the
    # exception of hyphens.
    lastpart_spaces = to_space_re.sub(' ', lastpart_minus_suffix)
    return capfirst(lastpart_spaces)


def template_choices(templates, display_names=None):
    """
    Given an iterable of `templates`, calculate human-friendly display names
    for each of them, optionally using the `display_names` provided, or a
    global dictionary (`TEMPLATE_DISPLAY_NAMES`) stored in the Django
    project's settings.

    .. note:: As the resulting iterable is a lazy generator, if it needs to be
              consumed more than once, it should be turned into a `set`, `tuple`
              or `list`.

    :param list templates: an iterable of template paths, as returned by
                           `find_all_templates`
    :param display_names: If given, should be a dictionary where each key
                          represents a template path in `templates`, and each
                          value is the display text.
    :type display_names: dictionary or None
    :return: an iterable of two-tuples representing value (0) & display text (1)
    :rtype: generator expression
    """
    # allow for global template names, as well as usage-local ones.
    if display_names is None:
        display_names = getattr(settings, 'TEMPLATE_DISPLAY_NAMES', {})


    return ((template, _fix_display_title(template_path=template,
                                          template_map=display_names))
            for template in templates)
