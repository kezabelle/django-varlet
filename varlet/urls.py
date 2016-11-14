# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.conf.urls import url
from .views import page_detail

page_detail_url = url(
    regex='^(?P<remaining_path>.*)/$',
    view=page_detail,
    name="page_detail",
    kwargs={}
)
page_index_url = url(
    regex='^$',
    view=page_detail,
    name="page_detail",
    kwargs={'remaining_path': ''}
)
current_app = "varlet"
urlpatterns = [
    page_detail_url,
    page_index_url,
]
