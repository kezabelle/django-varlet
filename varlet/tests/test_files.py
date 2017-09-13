# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import pytest


@pytest.mark.parametrize("filename,exists", (
    ('varlet/templates/django/forms/widgets/urlpath-autocomplete.html', True),
    ('varlet/templates/search/indexes/varlet/page_text.txt', True),
    ('varlet/static/varlet/riot.min.js', True),
    ('varlet/static/varlet/urlpath-autocomplete.tag', True),
    ('varlet/static/varlet/urlpath-autocomplete.css', True),
    ('varlet/static/varlet/urlpath-autocomplete.js', True),
    ('varlet/tests/templates/django/forms/widgets/urlpath-autocomplete.html', False),
))
def test_make_sure_files_exist_in_the_right_places(filename,exists):
    from django.conf import settings
    path = os.path.join(settings.BASE_DIR, filename)
    assert os.path.exists(path) is exists
    assert os.path.isfile(path) is exists
