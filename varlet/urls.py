# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.conf.urls import url
from varlet.views import PageViewSet


page_detail = PageViewSet.as_view(actions={
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
    'put': 'update'
}, suffix="Instance")
page_root = PageViewSet.as_view(actions={
    'post': 'create',
    'get': 'list'
}, suffix="List")


page_detail_url = url(
    r'^(?P<{lookup_url_kwarg}>{lookup_value})/$'.format(lookup_url_kwarg=PageViewSet.lookup_url_kwarg, lookup_value=PageViewSet.lookup_value_regex),
    page_detail,
    name="page-detail"
)
page_root_url = url(r'^$', page_root, name="page-list")

urlpatterns = [
    page_detail_url,
    page_root_url,
]
