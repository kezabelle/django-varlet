# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from .haystack_views import HaystackPageViewSet

__all__ = ['page_detail_url', 'page_root_url', 'urlpatterns']

page_detail_url = HaystackPageViewSet.as_detail_url()
page_root_url = HaystackPageViewSet.as_root_url()

urlpatterns = [
    page_detail_url,
    page_root_url,
]
