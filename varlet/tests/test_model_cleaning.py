# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import pytest
import swapper
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text


def test_url_including_non_path_chars_raises_error():
    Page = swapper.load_model('varlet', 'Page')
    p = Page(url='/this/will/#break/yo/', template='varlet/pages/layouts/test_template.html')
    with pytest.raises(ValidationError) as exc:
        p.full_clean()
    assert "Unsafe characters detected" in force_text(exc.value)


def test_url_including_escape_chars_raises_error():
    Page = swapper.load_model('varlet', 'Page')
    p = Page(url='/this/will/&lol/', template='varlet/pages/layouts/test_template.html')
    with pytest.raises(ValidationError) as exc:
        p.full_clean()
    assert "Unsafe characters detected" in force_text(exc.value)
