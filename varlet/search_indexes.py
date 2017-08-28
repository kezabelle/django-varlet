# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import swapper
from haystack.constants import Indexable
from haystack.fields import CharField, MultiValueField, DateTimeField
from haystack.indexes import SearchIndex


class BasePageIndex(SearchIndex):
    text = CharField(document=True, use_template=True, template_name='search/indexes/varlet/page_text.txt')
    url = CharField(model_attr='url')
    get_absolute_url = CharField(model_attr='get_absolute_url')
    template = MultiValueField(model_attr='get_template_names')
    created = DateTimeField(model_attr='created')

    def get_model(self):
        return swapper.load_model('varlet', 'page')

class PageIndex(BasePageIndex, Indexable):
    pass
