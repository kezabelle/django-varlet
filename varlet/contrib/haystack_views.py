# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import swapper
from haystack.query import SearchQuerySet
from haystack.backends import SQ
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from varlet.views import PageViewSet


class ExtendedSearchQuerySet(SearchQuerySet):
    def __init__(self, using=None, query=None):
        super(ExtendedSearchQuerySet, self).__init__(using=using, query=query)
        self.model = swapper.load_model('varlet', 'Page')
        self.query.add_model(self.model)

    def get(self, *args, **kwargs):
        clone = self._clone()
        clone.query.add_filter(SQ(*args, **kwargs))
        final = tuple(clone[0:2])
        final_count = len(final)
        if final_count > 1:
            raise MultipleObjectsReturned("Got {} results, expected 1".format(final_count))
        elif final_count == 0:
            raise self.model.DoesNotExist("No results for query")
        return final[0]


class HaystackPageViewSet(PageViewSet):
    queryset = ExtendedSearchQuerySet()
