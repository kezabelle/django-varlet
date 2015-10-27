# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import PageDetail, Homepage


page_view = url(regex=r'^(?P<slug>[-\w]+)/$',
                view=PageDetail.as_view(),
                name='view')

page_index = url(regex=r'^$',
                 view=Homepage.as_view(),
                 name='index')

urlpatterns = (page_view, page_index)
