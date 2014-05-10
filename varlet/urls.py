# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import PageDetail, IndexPage

urlpatterns = (
    url(regex=r'^(?P<slug>[-\w]+)/$',
        view=PageDetail.as_view(),
        name='view'),

    url(regex=r'^$',
        view=Homepage.as_view(),
        name='index'),
)
