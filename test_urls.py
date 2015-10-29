# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from varlet import named_urls
from varlet import get_version
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^page/{version}/'.format(version=get_version()),
        include(named_urls)),
    url(r'^$', RedirectView.as_view(permanent=False,
                                    pattern_name='pages:index')),
]
