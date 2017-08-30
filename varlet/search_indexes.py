# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import swapper
from haystack.constants import Indexable
from haystack.fields import CharField, DateTimeField
from haystack.indexes import SearchIndex


class BasePageIndex(SearchIndex):
    text = CharField(document=True, use_template=True, template_name='search/indexes/varlet/page_text.txt')
    url = CharField(model_attr='url')
    get_absolute_url = CharField(model_attr='get_absolute_url')
    created = DateTimeField(model_attr='created')
    modified = DateTimeField(model_attr='modified')

    def get_model(self):
        return swapper.load_model('varlet', 'page')

class PageIndex(BasePageIndex, Indexable):
    template = CharField(model_attr='template')
    template_title = CharField(model_attr='get_template_display')
    get_template_display = CharField(model_attr='get_template_display')
