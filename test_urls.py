# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.contrib import admin
from varlet import named_urls
from varlet import get_version


urlpatterns = patterns('',
    url(r'^admin_mountpoint/', include(admin.site.urls)),
    url(r'^page/{version}/'.format(version=get_version()),
        include(named_urls)),
)
